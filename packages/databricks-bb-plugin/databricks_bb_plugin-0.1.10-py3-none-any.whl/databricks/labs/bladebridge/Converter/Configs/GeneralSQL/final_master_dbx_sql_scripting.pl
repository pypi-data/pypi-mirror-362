use strict;
no strict 'refs';
use Globals;
use Data::Dumper;
use Common::MiscRoutines;
use DWSLanguage;

my $MR = new Common::MiscRoutines(MESSAGE_PREFIX => 'CUST_HOOK', DEBUG_FLAG => $Globals::ENV{CLI_OPT}->{v});
my $LAN = new DWSLanguage();
my %CFG = (); #entries to be initialized
my $CFG_POINTER = undef;
my $SOURCE_DIALECT = 'DEFAULT';
my $CONVERTER = undef;
my $STATIC_STRINGS = {};
my $COMMENTS = {};
my $CASE_WHEN = {};
my $FNAME;
my @FOR_LOOP_NAMES = ();
my $PRECISION_SCALE_DATA_TYPE_MAPPING =
{
	'\b(DECIMAL)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__',
	'\b(DEC)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)'  => 'DECIMAL__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__',
	'\b(NUMERIC)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => 'DECIMAL__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__',
	'\b(NUMBER)\s*\(\s*(\w+)\s*\,\s*(\w+)\s*\)' => 'DECIMAL__OPEN_PARENTHESIS__$2__COMMA__$3__CLOSE_PARENTHESIS__',
	'\b(FLOAT)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__',
	'\b(REAL)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__',
	
	'\b(TIMESTAMP)\s*\(\s*(\w+)\s*\)' => 'TIMESTAMP',
	# '\b(TIMESTAMP)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__',
	'\b(DATETIME2)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__',
	'\b(TIME)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__',
	
	'\[?\s*(\bNVARCHAR\b)\s*\]?\s*\(\s*(\w+)\s*\)' => ' STRING',
	'\[?\s*(\bVARCHAR\b)\s*\]?\s*\(\s*(\w+)\s*\)' => ' STRING',
	'\b(NCHAR)\s*\(\s*(\w+)\s*\)' => 'STRING',
	'\b(CHAR)\s*\(\s*(\w+)\s*\)' => '$1__OPEN_PARENTHESIS__$2__CLOSE_PARENTHESIS__'
};

sub handler_master_dbx_sql_scripting_prescan
{
	my $fname = shift;
	$MR->log_msg("handler_prescan: Processing file $fname");
	my $cont = $MR->read_file_content($fname) or die "Cannot open file $fname - $!";
	
	$FNAME = $fname;

	($cont, $STATIC_STRINGS, $COMMENTS) = $MR->collect_comments_and_static_strings($cont);
	
	$cont = delete_sql_comment($cont);

	foreach my $p (keys %$PRECISION_SCALE_DATA_TYPE_MAPPING)
	{
		if($cont =~ /$p/i)
		{
			while ($cont =~ s/$p/$PRECISION_SCALE_DATA_TYPE_MAPPING->{$p}/i)
			{
				my @tokk = ($1,$2,$3,$4,$5,$6,$7,$8,$9);
				my $idxx = 1;
				foreach my $too (@tokk)
				{
					$cont =~ s/\$$idxx/$too/g;
					$idxx++;
				}
			}
		}		
	}

	# initialize global BB hash
	$Globals::ENV{HOOKS} = {}; # reset before prcessing each file
	# check if there is a proc definition with params
	if ($cont =~ /\b(create|alter|replace)\b(\s+or\s+replace)*\s+(procedure|proc)\s+((\[.*?\]|\w+)\.?(\[.*?\]|\w+)*\.?(\[.*?\]|\w+)*)\s*(.*?)\s*(.*)/is)
	{
		my ($proc_name, $proc_params) = ($4, $9);
		# $proc_params = $MR->get_function_call($proc_params, 0);
		# $MR->log_error($proc_params);
		$MR->log_msg("Found proc '$proc_name' in file $fname");

		$Globals::ENV{HOOKS}->{PROC_FLAG} = 1;
		$proc_name = convert_static_string($proc_name);
		$proc_name =~ s/(\[|\])/`/g;
		$Globals::ENV{HOOKS}->{PROC_NAME} = $proc_name;
		collect_proc_params($proc_params);
	}
	elsif($cont =~ /\b(create|alter|replace)\b(\s+or\s+replace)*\s+function\s+([\w|.|\[|\]]+)\s*(.*?)\s*(.*?)\b(RETURN|RETURNS)\b\s+(\w+)/is)
	{
		my ($func_name, $func_params, $return_type) = ($3, $5, $7);
		$MR->log_msg("Found function '$func_name' in file $fname");

		$Globals::ENV{HOOKS}->{FUNC_FLAG} = 1;
		$func_name = convert_static_string($func_name);
		$Globals::ENV{HOOKS}->{FUNC_NAME} = $func_name;
		$Globals::ENV{HOOKS}->{RETURN_TYPE} = $return_type;
		collect_proc_params($func_params);
	}
	else
	{
		$Globals::ENV{HOOKS}->{PROC_FLAG} = 0;
		$Globals::ENV{HOOKS}->{FUNC_FLAG} = 0;
	}
	
	collect_temp_tables($cont);
	collect_table_variables($cont);
	collect_scalar_variables($cont);

	$MR->log_msg("PRESCAN: " . Dumper($Globals::ENV{HOOKS}));
	return $Globals::ENV{HOOKS}; # return something, since the converter class is expecting a hash
}

sub collect_proc_params
{
	my $proc_params = shift;

	if($proc_params =~ /\(?(.*?)(\)|\bAS\b|\bIS\b)/is)
	{
		$proc_params = $1;
		$proc_params =~ s/\bDEFAULT\b/=/gi;
	}

	if(!$proc_params || $proc_params eq '')
	{
		return;
	}

	my @arr_proc_params = $MR->get_direct_function_args($proc_params);
	$MR->log_msg("proc params array: " . Dumper(\@arr_proc_params));
	my $param_num = 0;

	foreach my $p (@arr_proc_params) # simplified/demo version.  will need to account for things like defaults, in/out params etc
	{
		$p =~ s/__OPEN_PARENTHESIS__/(/gis;
		$p =~ s/__CLOSE_PARENTHESIS__/)/gis;
		$p =~ s/__COMMA__/,/gis;

		$param_num++;
		my @tok = split(/\s+/, $p);

		my $type = 'IN';
		my $data_type;
		my $default_value;
		my $index = 0;

		my $param_name = undef;
		foreach (@tok)
		{
			if($_ eq '=')
			{
				$data_type = $tok[$index-1];
				$default_value = convert_static_string($tok[$index+1]);
			}
			if($MR->pos_in_list(lc($_),['in','input','out','output','inout']))
			{
				$type = uc($_);
				$type =~ s/input/in/i;
				$type =~ s/output/out/i;
				$index += 1;
				next;
			}
			elsif(!$data_type && $index == $#tok)
			{
				$data_type = $tok[$index];
			}
			if(!$param_name)
			{
				$param_name = $_;
			}
			$index += 1;
		}
		# arbitrarily add params to a global hash so later we can construct widgets
		$Globals::ENV{HOOKS}->{PROC_PARAM}->{$param_num} = {Name => $param_name, Type => $type, DataType => $data_type, default_value => $default_value};
		push(@{$Globals::ENV{HOOKS}->{VAR_NAMES}}, $tok[0]);
	}
}

sub collect_temp_tables
{
	my $text = shift;

	# custom replaces for teradata temp tables
	$text =~ s/\bVOLATILE\s+MULTISET\s+TABLE\b/TEMPORARY TABLE/gis;
	$text =~ s/\bMULTISET\s+VOLATILE\s+TABLE\b/TEMPORARY TABLE/gis;
	$text =~ s/\bSET\s+VOLATILE\s+TABLE\b/TEMPORARY TABLE/gis;
	$text =~ s/\bVOLATILE\s+SET\s+TABLE\b/TEMPORARY TABLE/gis;
	$text =~ s/\bVOLATILE\s+TABLE\b/TEMPORARY TABLE/gis;
	# custom replaces for teradata temp tables

	# check if there is a temp table
	while ($text =~ /\b(create|alter|replace)\b(\s+or\s+replace)*\s+(GLOBAL\s+)*(TEMP|TEMPORARY)\s+TABLE\s+([\w|.|\[|\]]+)\s*(.*?)\s*(.*)/gis)
	{
		my $temp_table = $5;
		$MR->log_msg("Found temp table '$temp_table' in file $FNAME");

		$temp_table = convert_static_string($temp_table);
		$Globals::ENV{HOOKS}->{TEMP_TABLES}->{$temp_table} = 1;
	}
	while($text =~ /\b(create\s+table)\b\s+(\#\#|\#)([\w|.|\[|\]]+)\s*(.*?)\s*(.*)/gis)#SQL Server
	{
		my $temp_table = $5;
		$MR->log_msg("Found temp table '$temp_table' in file $FNAME");

		$temp_table = convert_static_string($temp_table);
		$Globals::ENV{HOOKS}->{TEMP_TABLES}->{$temp_table} = 1;
	}
}

# table variables exist for SQL Server and Oracle
sub collect_table_variables
{
	my $cont = shift;

	# check if there is a table variable
	while ($cont =~ /(\@\w+)\s+Table/gis) #SQL Server, Synapse
	{
		my $temp_table = $5;
		$MR->log_msg("Found temp table '$temp_table' in file $FNAME");

		$temp_table = convert_static_string($temp_table);
		$Globals::ENV{HOOKS}->{TEMP_TABLES}->{$temp_table} = 1;
	}
	while($cont =~ /\bTYPE\s+(\w+)\s+IS\s+TABLE\s+OF\b/gis) #Oracle
	{
		my $table = $1;
		$MR->log_msg("Found table variable '$table' in file $FNAME");
		$Globals::ENV{HOOKS}->{TABLE_VARIABLES}->{$table} = 1;
	}
}

sub process_declare_block
{
	my ($block, $is_sql_synapse_var, $var_num) = @_;
	my @vars = split /[,;]/, $block;
	foreach my $var (@vars)
	{
		my $var_name;
		my $data_type;
		my $default_value;
		if($is_sql_synapse_var)
		{
			if ($var =~ /(\@\w+)\s+([\w\(\)]+)(?:\s*=\s*([^,;]+))?/i)
			{
				($var_name, $data_type, $default_value) = ($1, $2, $3);
			}
		}
		else
		{
			$block =~ /^\w+\s+\w+\s*\:?=?\s*.*/is;
			($var_name, $data_type, $default_value) = ($1, $2, $3);
		}
		if($Globals::ENV{HOOKS}->{TABLE_VARIABLES}->{$var_name})
		{
			next;
		}

		$var_num += 1;
		$default_value = convert_static_string($default_value);
		$data_type =~ s/__OPEN_PARENTHESIS__/(/gis;
		$data_type =~ s/__CLOSE_PARENTHESIS__/)/gis;
		$data_type =~ s/__COMMA__/,/gis;
		$Globals::ENV{HOOKS}->{SCALAR_VARIABLES}->{$var_num} = {Name => $var_name, DataType => $data_type, default_value => $default_value};
	}
	return $var_num;
}

sub collect_scalar_variables
{
	my $text = shift;

	my $var_num = 0;

	# Oracle, Postgres
	if($text =~ /\bDECLARE\s+(\w+.*?)\s+\bBEGIN\b/is)
	{
		my $var_declare = $1;
		my @vars = split /\;/, $var_declare;
		foreach my $v (@vars)
		{
			$var_num = process_declare_block($v, 0, $var_num);
		}
	}
	
	# SQL Server, Synapse
	if($text =~ /\bDECLARE\s*\@\w+/is)
	{
		my @lines = split /\n/, $text;
		my $in_declare = 0;
		my $declare_block = '';
		foreach my $line (@lines)
		{
			if ($line =~ /^\s*DECLARE\b/i)
			{
				$in_declare = 1;
				$line =~ s/^\s*DECLARE\s*//i;  # Remove DECLARE
				$declare_block .= $line;
				next;
			}
			if ($in_declare)
			{
				if ($line =~ /^\s*(SELECT|BEGIN|CREATE|INSERT|UPDATE|DELETE|MERGE|EXEC|WITH|ALTER|DROP|SET)\b/i)
				{
					$in_declare = 0;
					$var_num = process_declare_block($declare_block, 1, $var_num);
					$declare_block = '';
				}
				else
				{
					$declare_block .= $line;
					if ($line =~ /\;/)
					{
						$in_declare = 0;
						$var_num = process_declare_block($declare_block, 1, $var_num);
						$declare_block = '';
					}
				}
			}
		}
	}
}

sub collect_case_when
{
    my $cont = shift;

    my $index = 0;
    my %allowed_charcter_before_case = (
        '(' => 1,
        '+' => 1,
        '-' => 1,
        '*' => 1,
        '/' => 1,
        ',' => 1,
        '=' => 1,
        '<' => 1,
        '>' => 1,
        ' ' => 1,
        "\r" => 1,
        "\t" => 1,
        "\n" => 1
    );

    my %allowed_charcter_before_case_end = (
        ')' => 1,
        "'" => 1,
        ']' => 1,
        '"' => 1,
        ' ' => 1,
        "\r" => 1,
        "\t" => 1,
        "\n" => 1
    );

    my $active_case_block = 0; # True if the current position in the script is inside case when block.
    my $is_active_case = 0; # True if the current position in the script is inside case word.
    my $active_case_end = 0; # True if the current position in the script is inside case_when's end word.
    my $buf = '';
    my $last_char = '';
    my $caught_string = '';
    my $current_line = '';
    my $case_count = 0;
    my $case_end_count = 0;
				
    foreach my $char (split('', $cont))
    {
        if($active_case_block)
        {
            if(!$active_case_end)
            {
                if($is_active_case)
                {
					if($case_count > 0)
					{
						$buf .= $char;
					}

                    if(lc($caught_string) eq 'c')
                    {
                        if(lc($char) eq 'a') # checks if after c comes a (for case)
                        {
                            $caught_string .= $char;
							if($case_count == 0)
							{
								$buf .= $char;
							}
                        }
                        else
                        {
							$is_active_case = 0;
                            $caught_string = '';
                            if($case_count == 0)
                            {
                                $active_case_block = 0;
                                $buf = '';
                            }
                        }
                    }
                    elsif(lc($caught_string) eq 'ca')
                    {
                        if(lc($char) eq 's') # checks if after ca comes s (for case)
                        {
                            $caught_string .= $char;
							if($case_count == 0)
							{
								$buf .= $char;
							}
                        }
                        else
                        {
							$is_active_case = 0;
                            $caught_string = '';
                            if($case_count == 0)
                            {
                                $active_case_block = 0;
                                $buf = '';
                            }
                        }
                    }
                    elsif(lc($caught_string) eq 'cas')
                    {
                        if(lc($char) eq 'e') # checks if after cas comes e (for case)
                        {
                            $caught_string .= $char;
							if($case_count == 0)
							{
								$buf .= $char;
							}
                        }
                        else
                        {
							$is_active_case = 0;
                            $caught_string = '';
                            if($case_count == 0)
                            {
                                $active_case_block = 0;
                                $buf = '';
                            }
                        }
                    }
                    elsif(lc($caught_string) eq 'case')
                    {
						$is_active_case = 0;
                        my $temp_str = $current_line . $char;
                        if($temp_str =~ /\bcase\b/i) # checks if caught string is case operator
                        {
							if($case_count == 0)
							{
								$buf .= $char;
							}
							$case_count += 1;
							$caught_string = '';
                        }
                        elsif($char eq '_')
                        {
                            if($cont =~ /\Q$current_line\E__COMMENTS__[0-9]+/i) # checks comments after case word
                            {
								if($case_count == 0)
								{
									$buf .= $char;
								}
								$case_count += 1;
								$caught_string = '';
                            }
                            else
                            {
                                $caught_string = '';
                                if($case_count == 0)
                                {
                                    $active_case_block = 0;
                                    $buf = '';
                                }
                            }
                        }
						elsif($current_line =~ /__COMMENTS__[0-9]+case\b/i) # checks comments before case word
						{
							if($case_count == 0)
							{
								$buf .= $char;
							}
							$case_count += 1;
							$caught_string = '';
						}
                        else
                        {
							$is_active_case = 0;
                            $caught_string = '';
                            if($case_count == 0)
                            {
                                $active_case_block = 0;
                                $buf = '';
                            }
                        }
                    }
                }
                else
                {
					$buf .= $char;
                }
            }
            else
            {
                if(lc($caught_string) eq 'e')
                {
                    if(lc($char) eq 'n') # checks if after e comes n (for case end)
                    {
                        $caught_string .= $char;
                    }
                    else
                    {
                        $active_case_end = 0;
                        $caught_string = '';
                    }
                    $buf .= $char;
                }
                elsif(lc($caught_string) eq 'en')
                {
                    if(lc($char) eq 'd') # checks if after en comes d (for case end)
                    {
                        $caught_string .= $char;
                    }
                    else
                    {
                        $active_case_end = 0;
                        $caught_string = '';
                    }
                        $buf .= $char;
                }
                elsif(lc($caught_string) eq 'end')
                {
					$active_case_end = 0;
					$caught_string = '';
                    my $temp_str = $current_line . $char;
                    if($temp_str =~ /\bend\b/is) # checks if caught string is case end operator
                    {
                        $case_end_count += 1;
                    }
                    elsif($char eq '_')
                    {
                        if($cont =~ /\Q$current_line\E__COMMENTS__[0-9]+/i) # checks comments after end word
                        {
                            $case_end_count += 1;
                        }
                        #else
                        #{
                        #    $active_case_end = 0;
                        #    $caught_string = '';
                        #}
                    }
					elsif($current_line =~ /__COMMENTS__[0-9]+end\b/i) # checks comments before end word
					{
						$case_end_count += 1;
					}
                    #else
                    #{
                    #    $active_case_end = 0;
                    #    $caught_string = '';
                    #}
                    if($case_count == $case_end_count)
                    {
                        $CASE_WHEN->{"__CASE_WHEN__$index"} = $buf;
                        $index += 1;
                        $buf = '';
                        $is_active_case = 0;
						$active_case_block = 0;
                        $active_case_end = 0;
                        $caught_string = '';
						$case_count = 0;
						$case_end_count = 0;
                    }
					else
					{
						$buf .= $char;
					}
                }
            }
        }
		if($char eq "\n")
		{
			$current_line = '';
		}
		else
		{
			$current_line .= $char;
		}
        if($caught_string eq '')
        {
			# It checks whether it can be the beginning of a word case.
            if(lc($char) eq 'c' && ( $allowed_charcter_before_case{$last_char} || $current_line =~ /__COMMENTS__[0-9]+c/i))
            {
                if (!$active_case_block)
				{
                    $buf .= $char;
                }
                $active_case_block = 1;
				$is_active_case = 1;
                $caught_string = $char;
            }
            elsif($active_case_block && lc($char) eq 'e' && ($allowed_charcter_before_case_end{$last_char} || $current_line =~ /__COMMENTS__[0-9]+e/i)) # It checks whether it can be the beginning of a word case end.
            {
                #$buf .= $char;
                $active_case_end = 1;
                $caught_string = $char;
            }
        }
        $last_char = $char;
    }
    foreach my $key (sort { $b cmp $a } keys %$CASE_WHEN)
    {
        $cont =~ s/\Q$CASE_WHEN->{$key}\E/$key/s;
    }
	$MR->log_msg("Collected case whens:" . Dumper($CASE_WHEN));
    return $cont;
}

sub delete_sql_comment
{
	my $text = shift;
	foreach my $comment (sort { $b cmp $a } keys %$COMMENTS)
	{
		if($text =~ /$comment/s)
		{
			$text =~ s/$comment//s;
			delete $COMMENTS->{$comment};
		}
	}
	return $text;
}

sub convert_sql_comment
{
	my $text = shift;
	foreach my $comment (sort { $b cmp $a } keys %$COMMENTS)
	{
		if($text =~ /$comment/s)
		{
			$text =~ s/$comment/$COMMENTS->{$comment}/s;
			delete $COMMENTS->{$comment};
		}
	}
	return $text;
}

sub convert_static_string
{
	my $text = shift;

	foreach my $s (sort { $b cmp $a } keys %$STATIC_STRINGS)
	{
		if($text =~ /$s/s)
		{
			$text =~ s/$s/$STATIC_STRINGS->{$s}/gs;
			delete $STATIC_STRINGS->{$s};
		}
	}
	return $text;
}

sub convert_case_when
{
	my $text = shift;
	foreach my $s (sort { $b cmp $a } keys %$CASE_WHEN)
	{
		if($text =~ /$s/s)
		{
			my $cw = $CONVERTER->convert_sql_fragment($CASE_WHEN->{$s});
			$text =~ s/$s/$cw/gs;
			delete $CASE_WHEN->{$s};
		}
	}
	return $text;
}

sub handler_master_dbx_init_hooks
{
	my $param = shift;
	%CFG = %{$param->{CONFIG}}; # static copy, if we want it
	$CFG_POINTER = $param->{CONFIG}; #live pointer to config hash, give the ability to modify config incrementally
	$Globals::ENV{CFG_POINTER} = \%CFG;
	$CONVERTER = $param->{CONVERTER};
	$SOURCE_DIALECT = uc($param->{SOURCE_DIALECT});
	if(!$SOURCE_DIALECT)
	{
		$SOURCE_DIALECT = 'DEFAULT';
	}
	$MR = new Common::MiscRoutines() unless $MR;
	@FOR_LOOP_NAMES = ();
	#print "INIT_HOOKS Called. MR: $MR. config:\n" . Dumper(\%CFG);
}

sub handler_master_dbx_preprocess_file
{
	my $array_cont = shift; # array ref
	$MR->log_msg("handler_master_dbx_preprocess_file: line count: " . scalar(@$array_cont));
	my $cont = join("\n", @$array_cont);
	#$MR->mask_sql_comments($cont);

	$Globals::ENV{COLLECT_SQL_ATTR} = undef;
	($cont, $STATIC_STRINGS, $COMMENTS) = $MR->collect_comments_and_static_strings($cont);
	$Globals::ENV{COLLECT_SQL_ATTR}->{STATIC_STRINGS} = $STATIC_STRINGS;
	$Globals::ENV{COLLECT_SQL_ATTR}->{COMMENTS} = $COMMENTS;
	$cont = collect_case_when($cont);
	
	foreach my $p (keys %$PRECISION_SCALE_DATA_TYPE_MAPPING)
	{
		if($cont =~ /$p/i)
		{
			while ($cont =~ s/$p/$PRECISION_SCALE_DATA_TYPE_MAPPING->{$p}/i)
			{
				my @tokk = ($1,$2,$3,$4,$5,$6,$7,$8,$9);
				my $idxx = 1;
				foreach my $too (@tokk)
				{
					$cont =~ s/\$$idxx/$too/g;
					$idxx++;
				}
			}
		}		
	}
	    
	$cont =~ s/\belse\s+if\b/elseif/gis;

	if($CFG_POINTER->{use_mark_separators})
	{
		$cont = mark_separators($cont);
	}
	
	$cont =~ s/\s+\;/;/gs;
	$cont =~ s/\;\s*\;/;/gs;

	if($CFG_POINTER->{prefix_for_variable})
	{
		foreach my $v (keys %{$Globals::ENV{HOOKS}->{SCALAR_VARIABLES}})
		{
			my $var_name = $Globals::ENV{HOOKS}->{SCALAR_VARIABLES}->{$v}->{Name};
			$var_name = s/^\@//;
			$cont =~ s/\@($var_name)\b/$CFG_POINTER->{prefix_for_variable}$1/g;
		}
		foreach my $v (keys %{$Globals::ENV{HOOKS}->{TABLE_VARIABLES}})
		{
			my $var_name = $Globals::ENV{HOOKS}->{TABLE_VARIABLES}->{$v}->{Name};
			$var_name = s/^\@//;
			$cont =~ s/\@($var_name)\b/$CFG_POINTER->{prefix_for_variable}$1/g;
		}
		foreach my $p (keys %{$Globals::ENV{HOOKS}->{PROC_PARAM}})
		{
			my $param_name = $Globals::ENV{HOOKS}->{PROC_PARAM}->{$p}->{Name};
			$param_name = s/^\@//;
			$cont =~ s/\@($param_name)\b/$CFG_POINTER->{prefix_for_variable}$1/g;
		}
	}
	if($Globals::ENV{HOOKS}->{PROC_FLAG})
	{
		$cont =~ s/\b(create|alter|replace)\b(\s+or\s+replace)*\s+(procedure|proc)\s+([\w|.|\[|\]]+)\s*(.*?)\s*\bAS(\s+\$\$)/PROC_HEADER\n\$\$\n/is;
		# $cont =~ s/\b(create|alter|replace)\b(\s+or\s+replace)*\s+(procedure|proc)\s+([\w|.|\[|\]]+)\s*(.*?)\s*\(?(.*?)(\)|\bAS\b|\bIS\b)/PROC_HEADER/is;
		$cont =~ s/\b(create|alter|replace)\b(\s+or\s+replace)*\s+(procedure|proc)\s+((\[.*?\]|\w+)\.?(\[.*?\]|\w+)*\.?(\[.*?\]|\w+)*)\s*(.*?)\s*\(?(.*?)(\)|\bAS\b|\bIS\b)/PROC_HEADER/is;
		my $proc_header = $CFG_POINTER->{procedure_header};
		$proc_header =~ s/\%PROCEDURE_NAME\%/$Globals::ENV{HOOKS}->{PROC_NAME}/;
		my $param_str = '';
		if($Globals::ENV{HOOKS}->{PROC_PARAM})
		{

			foreach my $p (sort { $a <=> $b } keys %{$Globals::ENV{HOOKS}->{PROC_PARAM}})
			{
				my $param = $Globals::ENV{HOOKS}->{PROC_PARAM}->{$p};
				if($CFG_POINTER->{prefix_for_variable})
				{
					$param->{Name} =~ s/^\@/$CFG_POINTER->{prefix_for_variable}/;
				}

				if($param_str ne '')
				{
					$param_str .= ",\n";
				}
				$param_str .= "$param->{Type} $param->{Name} $param->{DataType}";
				if($param->{default_value})
				{
					$param_str .= " DEFAULT $param->{default_value}";
				}
			}
		}
		$proc_header =~ s/\%PARAMETERS\%/$param_str/;
		$cont =~ s/PROC_HEADER/$proc_header/is;
		$cont =~ s/\bBEGIN\b/BEGIN;/is;
	}
	elsif($Globals::ENV{HOOKS}->{FUNC_FLAG})
	{
		$cont =~ s/\b(create|alter|replace)\b(\s+or\s+replace)*\s+function\s+([\w|.|\[|\]]+)\s*(.*?)\s*(.*?)\b(RETURN|RETURNS)\b\s+.*?\bBEGIN\b/FUNC_HEADER\nBEGIN\n/is;
		# $cont =~ s/\b(create|alter|replace)\b(\s+or\s+replace)*\s+(procedure|proc)\s+((\[.*?\]|\w+)\.?(\[.*?\]|\w+)*\.?(\[.*?\]|\w+)*)\s*(.*?)\s*\(?(.*?)(\)|\bAS\b|\bIS\b)/PROC_HEADER/is;
		my $func_header = $CFG_POINTER->{defined_function_header};
		$func_header =~ s/\%FUNCTION_NAME\%/$Globals::ENV{HOOKS}->{FUNC_NAME}/;
		my $param_str = '';
		if($Globals::ENV{HOOKS}->{PROC_PARAM})
		{

			foreach my $p (sort { $a <=> $b } keys %{$Globals::ENV{HOOKS}->{PROC_PARAM}})
			{
				my $param = $Globals::ENV{HOOKS}->{PROC_PARAM}->{$p};
				if($CFG_POINTER->{prefix_for_variable})
				{
					$param->{Name} =~ s/^\@/$CFG_POINTER->{prefix_for_variable}/;
				}

				if($param_str ne '')
				{
					$param_str .= ",\n";
				}
				$param_str .= "$param->{Name} $param->{DataType}";
				if($param->{default_value})
				{
					$param_str .= " DEFAULT $param->{default_value}";
				}
			}
		}
		$func_header =~ s/\%PARAMETERS\%/$param_str/;
		$func_header =~ s/\%RETURN_TYPE\%/$Globals::ENV{HOOKS}->{RETURN_TYPE}/;
		
		$cont =~ s/FUNC_HEADER/$func_header/is;
		$cont =~ s/\bBEGIN\b/BEGIN;/is;
	}

	# for oracle/netezza
	$cont =~ s/^(\s*)(\w+\s+)(\:\=)/$1SET $2$3/gm;
	$cont =~ s/\:\=/=/gm;

	$cont =~ s/\bBEGIN\s+TRY\b/BEGIN_TRY/gis;
	$cont =~ s/\bEND\s+TRY\b/END_TRY/gis;
	$cont =~ s/\bBEGIN\s+CATCH\b/BEGIN_CATCH/gis;
	$cont =~ s/\bEND\s+CATCH\b/END_CATCH/gis;
	
    $cont =~ s/\bDROP\s+FUNCTION\s+IF\s+EXISTS\b.*//gi;
    $cont =~ s/\bDROP\s+PROCEDURE\s+IF\s+EXISTS\b.*//gi;
    $cont =~ s/\bBEGIN\s+/BEGIN\n/gi;
    $cont =~ s/\bELSE\s+/ELSE\n/gi;

    $cont =~ s/\bIF\s+OBJECT_ID\s*\(.*?\)\s+IS\s+NOT\s+NULL\b//gis;
	$cont =~ s/\bIF\s+object_id\b/IF_object_id/gi; #ms sql approach

    $cont = change_begin_end_to_then_end_if($cont);
    $cont = change_while_begin_end_to_do_end_while($cont);
    $cont = change_for_loop_for_dbx_sql($cont);
    $cont = oracle_procedure_variable_processing($cont);
    $cont = snowflake_procedure_variable_processing($cont);

    $cont =~ s/(\bdrop\s+table\b) (?!IF\b)/DROP_TABLE_IF_EXISTS /gis;
	$cont =~ s/\bIF_object_id\b/IF object_id/gi; #ms sql approach

    $cont =~ s/(\bTHEN\b\s*)\;/$1/gis;
    $cont =~ s/(\bTHEN\b)(\s*)/$1;$2/gis;

    my @ret = split(/\n/, $cont);
    $MR->log_msg("NEW CONT: $cont");
    return @ret;

}


# fragmend handlers
sub var_declare
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("var_declare: $cont");
	
	if($cont =~/(.*?)(\bDECLARE\s+.*)/is)
	{
		my $pre = $1;
		my $declare_str = $2;
		my @declares = split /\,/,$declare_str;
		my $corrected_declare = '';
		foreach my $declare (@declares)
		{
			$declare = $MR->trim($declare);
			$declare =~ s/^\bdeclare\b//is;
			$declare = $MR->trim($declare);
			$corrected_declare .= "declare variable $declare;\n";
		}
		$cont = $pre . $corrected_declare;
	}

	if($cont =~/(.*?)\bDECLARE\s+VARIABLE\s+(\w+).*?\=\s*(.*)/is)
	{
		my $pre = $1;
		my $var = $2;
		my $val = $3;
		if(is_func($val))
		{
			$cont =~ s/\=\s*(.*)/;/s;
			$cont .= "\nSET $var = $val";
		}
	}
	$cont = $CONVERTER->convert_sql_fragment($cont);
	return $cont;
}

sub set_in_select
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("set_in_select: $cont");
	$cont =~/\bselect\b\s+(\w+\s*\=.*?)\bFROM/is;
	my $set_str = $1;
	my @sets = split /\,/,$set_str;
	my $final_set = '';
	my $ret = '';
	$cont =~ /(.*?)\bselect\b\s+\w+\s*\=.*?(\bFROM\b.*)\;/is;
	my $pre_select = $1;
	my $post_from = $2;
	
	foreach my $set (@sets)
	{
		if($ret ne '')
		{
			$ret .= "\n";
		}
		$set =~ /(.*?)\s*\=(.*)/is;
		$ret = $pre_select."SET ". $MR->trim($1) . " = (\nSELECT\n".$MR->trim($2).$post_from.');';

	}

	$ret = $CONVERTER->convert_sql_fragment($ret);
	return $ret;
}

sub start_for_loop
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("start_for_loop: $cont");
	$cont =~ /(\w+)\:\s+\bfor\b/is;
	my $for_loop_name = $1;
	if($for_loop_name)
	{
		push(@FOR_LOOP_NAMES, $for_loop_name);
	}
	$cont = $CONVERTER->convert_sql_fragment($cont);
	return $cont;
}

sub continue_for_loop
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("continue_for_loop: $cont");
	my $for_loop_name = '';
	if($#FOR_LOOP_NAMES > -1)
	{
		$for_loop_name = $FOR_LOOP_NAMES[-1];
	}

	$cont =~ s/\bcontinue\b/ITERATE $for_loop_name/is;
	$cont = $CONVERTER->convert_sql_fragment($cont);
	return $cont;
}

sub exit_for_loop
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("exit_for_loop: $cont");
	my $for_loop_name = '';
	if($#FOR_LOOP_NAMES > -1)
	{
		$for_loop_name = $FOR_LOOP_NAMES[-1];
	}
	
	$cont =~ s/\bexit\b/LEAVE $for_loop_name/is;
	$cont = $CONVERTER->convert_sql_fragment($cont);
	return $cont;
}

sub end_for_loop
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("end_for_loop: $cont");
	pop(@FOR_LOOP_NAMES);
}

sub select_into_var
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);
	$MR->log_msg("select_into_var: $cont");
	my $ret = '';
	if($cont =~ /(.*?)\bselect\b\s+(.*?)\s*\bINTO\b\s+(.*?)\s*(\bFROM\b.*)\;/is)
	{
		$ret = $1."SET ".$MR->trim($3)." = (\nSELECT\n" . $MR->trim($2) . "\n" . $4 . ');';
	}
	elsif($cont =~ /(.*?)\bselect\b\s+(.*?)\s*(\bFROM\b.*)\bINTO\b\s+(.*?)\s*\;/is)
	{
		my $pre_select = $1;
		my $columns_str = $2;
		my @columns = split /\,/,$columns_str;
		my $post_from = $3;
		my @variables = split /\,/,$4;
		$ret = $pre_select;
		for(my $i; $i < @columns; $i++)
		{
			if($ret ne '')
			{
				$ret .= "\n";
			}

			$ret .= $pre_select."SET ". $variables[$i] . " = (\nSELECT\n".$columns[$i]."\n".$post_from.');';
		}

	}
	elsif($cont =~ /(.*?)\bselect\b\s+(.*?)\s*\bINTO\b\s+(.*?)\s*\;/is)
	{
		$ret = $1;
		my @variables = split(/\,/, $MR->trim($3));
		my @values = split(/\,/, $MR->trim($2));
		for (my $i; $i < @variables; $i++)
		{
			$ret .= "SET $variables[$i] = $values[$i];\n";
		}
	}

	$ret = $CONVERTER->convert_sql_fragment($ret);
	return $ret;
}


sub finalize_content
{
	my $array_cont = shift; # array ref
	my $cont = join("\n", @$array_cont);

	$cont = ordering_variable_declaration($cont);
	$cont = convert_case_when($cont);
	$cont = convert_static_string($cont);
	$cont = convert_sql_comment($cont);
	
	# if($CFG_POINTER->{use_mark_separators})
	# {
		$cont =~ s/\;\s*\;/;/gs;
	# }

	$cont =~ s/\'\\\'/'\\\\'/g;
	$cont =~ s/\"\\\"/"\\\\"/g;
	
	$cont =~ s/(\bDO\b\s*)\;/$1/gis;
	$cont =~ s/(\bBEGIN\b\s*)\;/$1/gis;
	$cont =~ s/(\bTHEN\b\s*)\;/$1/gis;
	$cont =~ s/(\bELSE\b\s*)\;/$1/gis;
	$cont =~ s/(\bAS\b\s*)\;/$1/gis;
	
	$cont =~ s/__OPEN_PARENTHESIS__/(/gis;
	$cont =~ s/__CLOSE_PARENTHESIS__/)/gis;
	$cont =~ s/__COMMA__/,/gis;
	
	$cont =~ s/BEGIN_TRY/BEGIN TRY/gis;
	$cont =~ s/END_TRY/END TRY/gis;
	$cont =~ s/BEGIN_CATCH/BEGIN CATCH/gis;
	$cont =~ s/END_CATCH/END CATCH/gis;
	$cont =~ s/\bPROC_FINISH\b/END;/gis;
	if($CFG_POINTER->{fix_me_on})
	{
		foreach my $f_patt (keys %{$CFG_POINTER->{source_platform}->{$SOURCE_DIALECT}})
		{
			$cont =~ s/($f_patt)/$1 \/*FIXME*\//gis;
		}
	}

	@$array_cont = split(/\n/, $cont);
}

# custom functions
sub is_func
{
    my $str = shift;
    if($str =~ /\(.*\)/)
	{
		return 1;
	}
    return 0;
}

# databricks sql syntax

# for if/else condition
sub change_begin_end_to_then_end_if
{
	my $content = shift;
	while($content =~ /(.*)(\bif\b.*?\bbegin\b.*)/is)
	{
		my $start_section = $1;
		my $last_if_condition = $2;
		if($last_if_condition =~ /(\bif\b.*?)\bbegin\b(.*?)\bend\b(.*?)(\belse\b.*?)\bbegin\b(.*?)\bend\b(.*)/is)
		{
			my $if_condition = $1;
			my $if_section = $2;
			my $section_between_if_else = $3;
			my $section_between_else_begin = $4;
			my $else_section = $5;
			my $last_part = $6;

			$content = $start_section.$if_condition.'THEN;'.$if_section.$section_between_if_else.$section_between_else_begin.$else_section.'END IF'.$last_part;
		}
		elsif($last_if_condition =~ /(\bif\b.*?)\bbegin\b(.*?)\bend\b(.*)/is)
		{
			my $if_condition = $1;
			my $if_section = $2;
			my $last_part = $3;

			$content = $start_section.$if_condition.'THEN;'.$if_section.'END IF'.$last_part;
		}
	}
	$content =~ s/\bEND IF\b( IF\b)+/END IF/gi;
	return  $content;
}

# for while loop
sub change_while_begin_end_to_do_end_while
{
	my $content = shift;
	while($content =~ /(.*)(\bwhile\b.*?\bbegin\b.*)/is) #ms sql synapse
	{
		my $start_section = $1;
		my $last_while_condition = $2;
		if($last_while_condition =~ /(\bwhile\b.*?)\bbegin\b(.*?)\bend\b(.*)/is)
		{
			my $while_condition = $1;
			my $while_section = $2;
			my $last_part = $3;

			$content = $start_section.$while_condition.'DO;'.$while_section.'END WHILE'.$last_part;
		}
	}
	while($content =~ /(.*)(\bwhile\b.*?\bloop\b.*)/is) #oracle
	{
		my $start_section = $1;
		my $last_while_condition = $2;
		if($last_while_condition =~ /(\bwhile\b.*?)\bloop\b(.*?)\bend\b\s+loop\b(.*)/is)
		{
			my $while_condition = $1;
			my $while_section = $2;
			my $last_part = $3;

			$content = $start_section.$while_condition.'DO;'.$while_section.'END WHILE'.$last_part;
		}
	}
	return  $content;
}

# for for loop
sub change_for_loop_for_dbx_sql
{
	my $content = shift;
	my $index = 1;

	$content =~ s/\bend\s+loop\b/END_LOOP/gis;
	while($content =~ /\n(\s*\bfor.*?\bin\b.*?\bloop\b)/is) #ms sql synapse
	{
		my $for_lopp_start = $1;
		$content =~ s/\n(\s*\bfor.*?\bin\b.*?)\bloop\b/\n for_loop_$index: $1 DO;/is;
		$index += 1;
	}
	while($content =~ /.*\n\s*(for_loop_[0-9]+)\:\s+(\bfor.*?\bin\b.*?\bDO\b.*?)\bEND_LOOP\b/is) #oracle
	{
		my $for_loop_name = $1;
		my $for_loop_body = $2;
		
		$content =~ s/($for_loop_name\b\:\s+\Q$for_loop_body\E)\bEND_LOOP\b/$1 end for $for_loop_name/is;
	}
	return  $content;
}

# for oracle polishing variables declare
sub oracle_procedure_variable_processing
{
	my $content = shift;
	if($content =~ /\bis\b(.*?)\bbegin\b/is)
	{
		my $variable_section = $1;
		$variable_section =~ s/^(\s*)(?!__comments__[0-9]+\b)(\w+.*)/$1 DECLARE $2/gim;
		$variable_section =~ s/\:\=/=/gi;

		$content =~ s/\bis\b.*?\b(begin\b\s*\;)/$1$variable_section/is
	}
	return  $content;
}

# for snowflake polishing variables declare
sub snowflake_procedure_variable_processing
{
	my $content = shift;
	if($content =~ /\bas\b\s*\$\$\s+\bDECLARE\b(.*?)\bbegin\b/is)
	{
		my $variable_section = $1;
		$variable_section =~ s/^(\s*)(?!__comments__[0-9]+\b)(\w+.*)/$1 DECLARE $2/gim;
		$variable_section =~ s/\:\=/=/gi;
		

		$content =~ s/(\bas\b)\s*\$\$\s+\bDECLARE\b.*?(\bbegin\b\;?)/$1\n$2\n$variable_section/is
	}
	return  $content;
}

# Variable can only be declared at the beginning of the compound.
sub ordering_variable_declaration
{
	my $content = shift;
	my @variables = $content =~ /\bdeclare\b.*\;/gim;
	$content =~ s/\bdeclare\b.*\;/__START_VARIABLES_DECLARE__/im;
	$content =~ s/\bdeclare\b.*\;//gim;
	my $variables_str = join("\n", @variables);
	$content =~ s/__START_VARIABLES_DECLARE__/$variables_str/gim;
	return  $content;
}

# MS SQL
sub mark_separators
{
    my $sql = shift; #scalar content of file

    $sql =~ s/END\s*GO\s*$/PROC_FINISH/gis;
    $sql =~ s/END\s*$/PROC_FINISH/gis;
    $sql =~ s/with\s+RECOMPILE//gis; #so it does not mess up our WITH logic

    my @prior_keywords = ('INSERT', 'UPDATE', 'DELETE', 'MERGE', 'ALTER', 'DROP', 'TRUNCATE', 'IF', 'WHILE', 'RETURN', 'BREAK', 'BEGIN\s+TRANSACTION', 'CREATE\s+TABLE', 'COMMIT', 'ROLLBACK', 'SAVE\s+TRANSACTION',
                          'DECLARE', 'EXEC', 'EXECUTE', 'USE', 'PRINT', 'WITH', 'GRANT', 'REVOKE', 'DENY');
    foreach my $keyword (@prior_keywords)
    {
        my $modified_keyword = $keyword;
        $modified_keyword =~ s/\\s\+/ /gi;

        $sql =~ s/\b$keyword\b/\;\n$modified_keyword/gi;
    }
    # set var
    $sql =~ s/(\bSET\s+\@\w+\s*\=)/\;\n$1/gi;

    
    # 'SELECT'
    
    return $sql;
}