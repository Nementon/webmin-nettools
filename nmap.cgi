#!/usr/bin/perl

#    Network Utilities Webmin Module - Nmap
#    Copyright (C) 1999-2003 by Tim Niemueller <tim@niemueller.de>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 31.08.1999

# Note to myself:
# this file is in a bad shape. Uses too many global vars. Try to clean up
# when time left

require './nettools-lib.pl';
&init_command('nmap');


%NmapTypes = (
    -sT         => $text{'nmap_tcpconnect'},
    -sS         => $text{'nmap_syn'},
    -sF         => $text{'nmap_stealth'},
    -sX         => $text{'nmap_xmastree'},
    -sN         => $text{'nmap_null'},
    -sP         => $text{'nmap_ping'},
    -sU         => $text{'nmap_udp'}
    );

&ReadParse();

$options = "";
for (keys %NmapTypes) {
        $options .= "<OPTION VALUE=\"$_\"";
        if ($in{'scantype'}) {
         $options .= $in{'scantype'} eq $_ ? " SELECTED" : "";
        } else {
         $options .= $_ eq "-sT" ? " SELECTED" : "";
        }
        $options .= ">$NmapTypes{$_}\n";
}


my $execline = "";
if ($in{'host'}) {
  &CheckAll();
}

$Errors="<H3><FONT COLOR=\"red\">\n";
foreach $tmperr (@error) {
 $Errors .= $tmperr . "<BR>";
}
$Errors .= '</FONT></H3>';

&header($text{'nmap_title'}, undef, undef, 0, 0, 0,
        "<a href=\"about.cgi\">$text{'about'}</a>");

if ($execline && !$critical_err) {

 print "<BR><BR>";
 if ($in{'nmap'}) { print &text('running', $text{'nmap_title'}) }

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";

 print "<PRE>\n$execline\n";
   open (CHILD, "$execline |");
    while (<CHILD>) {
     print $_;
    }
   close (CHILD);
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";

} elsif ($critical_err) {
 print "<BR><BR>";
 if ($in{'nmap'}) { print &text('error_crit', "Nmap") }

 print "<HR SIZE=4 NOSHADE ALIGN=center>\n$Errors";
 print "</PRE>\n<HR SIZE=4 NOSHADE ALIGN=center>\n\n";
}

print <<EOM;

<br/>
<FORM METHOD="POST" ACTION="$progname">

<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR><TD>
<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>$text{'hostname'}:</TD>
<TD><INPUT TYPE=text NAME="host" SIZE=20 VALUE="$in{'host'}"></TD>
<TD>$text{'nmap_scantype'}:</TD>
<TD><SELECT NAME="scantype">$options</SELECT></TD>
</TR></TABLE>
</TD></TR>
<tr><td><br/>&nbsp;</td></tr>
<TR><TD><TABLE BORDER=0 CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
EOM

print "<TR><TD><INPUT TYPE=checkbox NAME=\"verbosity\" VALUE=\"1\"";
if ($in{'verbosity'}) { print " checked" }
print "> $text{'nmap_verbout'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"p0\" VALUE=\"1\"";
if ($in{'p0'}) { print " checked" }
print "> $text{'nmap_noping'}</TD></tr>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"pa\" VALUE=\"1\"";
if ($in{'pa'}) { print " checked" }
print "> $text{'nmap_ackport'}: <INPUT TPYE=text NAME=\"paport\" VALUE=\"$in{'paport'}\" SIZE=5> </TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"pi\" VALUE=\"1\"";
if ($in{'pi'}) { print " checked" }
print "> $text{'nmap_ping'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"pb\" VALUE=\"1\"";
if ($in{'pb'}) { print " checked" }
print "> $text{'nmap_ackping_parallel'}</TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"o\" VALUE=\"1\"";
if ($in{'o'}) { print " checked" }
print "> $text{'nmap_osdet'}</TD></TR>";

print "<TD><INPUT TYPE=checkbox NAME=\"f\" VALUE=\"1\"";
if ($in{'f'}) { print " checked" }
print "> $text{'nmap_tinyfrag'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"p\" VALUE=\"1\"";
if ($in{'p'}) { print " checked" }
print "> $text{'nmap_scanports'}: <INPUT TPYE=text NAME=\"ports\" VALUE=\"$in{'ports'}\" SIZE=30> </TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"fast\" VALUE=\"1\"";
if ($in{'fast'}) { print " checked" }
print "> $text{'nmap_fastscan'}</TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"d\" VALUE=\"1\"";
if ($in{'d'}) { print " checked" }
print "> $text{'nmap_decoys'}: <INPUT TYPE=text NAME=\"decoys\" SIZE=30></TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"e\" VALUE=\"1\"";
if ($in{'e'}) { print " checked" }
print "> $text{'nmap_interface'}: <INPUT TYPE=text NAME=\"iface\" SIZE=5 VALUE=\"$in{'iface'}\"></TD></TR>";

print "<TR><TD><INPUT TYPE=checkbox NAME=\"g\" VALUE=\"1\"";
if ($in{'g'}) { print " checked" }
print "> $text{'nmap_sport'}: <INPUT TYPE=text NAME=\"sport\" SIZE=5 VALUE=\"$in{'sport'}\"></TD>";

print "<TD><INPUT TYPE=checkbox NAME=\"m\" VALUE=\"1\"";
if ($in{'m'}) { print " checked" }
print "> $text{'nmap_maxsock'}: <INPUT TYPE=text NAME=\"sockets\" SIZE=5 VALUE=\"$in{'sockets'}\"></TD></TR>";

print <<EOM;
</TABLE>
</td></tr></table>
<br/>
<INPUT TYPE=submit VALUE="   $text{'lib_nmap'}   " NAME="nmap">
</FORM>
<br/>
EOM



&footer("index.cgi", $text{'nmap_return'});


sub CheckAll {

  @error="";
  my @allowed_scantypes = ('-sN', '-sP', '-sS', '-sT', '-sU', '-sX', '-sF');

  &terror('error_badchar', $in{'scantype'}) if (defined($in{'scantype'}) && !(grep $_ eq $in{'scantype'}, @allowed_scantypes));
  &terror('error_badchar', $in{'host'}) if (defined($in{'host'}) && $in{'host'} =~ /[^\w\-\.]/);
  &terror('traceroute_err_iface', $in{'iface'}) if (defined($in{'iface'}) && !($in{'iface'} eq '') && (length $in{'iface'} > 6 || $in{'iface'} !~ /^[a-zA-Z0-9]+$/ ));

  # Check host, or IP
  if ($in{'host'} eq '') {
    push(@error, "$text{'error_nohost'}\n");
	$critical_err = 1;
  } elsif (length $in{'host'} > 64) {
    push(@error, "$text{'error_longhostname'}\n");
	$critical_err = 1;
  } elsif ($in{'host'} =~ /[^\w\-\.]/) {
    push(@error, &text('error_badchar', $in{'host'})."\n");
	$critical_err = 1;
  }

  if (! $in{'scantype'} ) {
    $in{'scantype'} = "-sT";
  }

  $nmap_opt="$in{'scantype'}";

  if ($in{'verbosity'}) { $nmap_opt .= " -v" }
  if ($in{'p0'}) { $nmap_opt .= " -P0" }

  if ($in{'pa'}) {
    $in{'paport'} =~ s/\ //g;
    if (!$in{'paport'}) {
      push(@error, $text{'nmap_err_ack'});
    } else {
      my $scanned_ports_optn = "";
      my @scanned_ports = ();
      my @ports = split(',', $in{'paport'});

      foreach my $port (@ports) {
        $port = $port + 0;
        if ($port <= 0) {
          &terror('nmap_err_lowport', $in{'paport'});
        }
        elsif ($port > 65535) {
          &terror('nmap_err_highport', $in{'paport'});
        }
        else {
          push(@scanned_ports, $port);
        }
      }

      $scanned_ports_optn = join(',', @scanned_ports);
      $nmap_opt .= " -PA$scanned_ports_optn";
    }
  }

  if ($in{'pi'}) { $nmap_opt .= " -PI" }
  if ($in{'pb'}) { $nmap_opt .= " -PB" }
  if ($in{'o'}) { $nmap_opt .= " -O" }
  if ($in{'f'}) { $nmap_opt .= " -f" }

  if ($in{'p'}) {
    $in{'ports'} =~ s/\ //g;
    if (!$in{'ports'}) {
      push(@error, $text{'nmap_err_port'});
    }
    else {
      my $scanned_ports_optn = "";
      my @scanned_ports = ();
      my @ports = split(',', $in{'ports'});

      foreach my $port (@ports) {
        $port = $port + 0;
        if ($port <= 0) {
          &terror('nmap_err_lowport', $in{'ports'});
        }
        elsif ($port > 65535) {
          &terror('nmap_err_highport', $in{'ports'});
        }
        else {
          push(@scanned_ports, $port);
        }
      }

      $scanned_ports_optn = join(',', @scanned_ports);
      $nmap_opt .= " -p $scanned_ports_optn";
    }
  }

  if ($in{'fast'}) { $nmap_opt .= " -F" }

  if ($in{'d'}) {
    $in{'decoys'} =~ s/\ //g;
    if (!$in{'decoys'}) {
      push(@error, $text{'nmap_err_decoys'});
    }
    else {
      my $decoys_optn = "";
      my @decoys = ();
      my @in_decoys = split(',', $in{'decoys'});

      foreach my $decoy (@in_decoys) {
        if (!&check_ipaddress($decoy)) {
          &terror('error_badchar', $in{'decoys'});
        } 
        else {
          push(@decoys, $decoy);
        }
      }

      $decoys_optn = join(',', @decoys);
      $nmap_opt .= " -D$decoys_optn";
    }
  }

  if ($in{'e'}) {
    $in{'iface'} =~ s/\ //g;
    if (!$in{'iface'}) {
      push(@error, $text{'nmap_err_iface'});
    }
    else {
      $nmap_opt .= " -e $in{'iface'}";
    }
  }

  if ($in{'g'}) {
    $in{'sport'} =~ s/\ //g;
    if (!$in{'sport'}) {
      push(@error, $text{'nmap_err_sport'});
    }
    else {
      my $src_port = $in{'sport'} + 0;
      $nmap_opt .= " -g $src_port";
    }
  }

  if ($in{'m'}) {
    $in{'sockets'} =~ s/\ //g;
    if (!$in{'sockets'}) {
      push(@error, $text{'nmap_err_maxsock'});
    }
    elsif ($in{'sockets'} < 0) {
      push(@error, $text{'nmap_err_lowsock'});
    }
    elsif ($in{'sockets'} > 16) {
      push(@error, $text{'nmap_err_bigsock'});
    }
    else {
      my $socket = $in{'sockets'} + 0;
      $nmap_opt .= " -M $socket";
    }
  }


  $execline ="$binary $nmap_opt $in{'host'} 2>&1";
  return $execline;
} # End Sub CheckAll

### End of nmap.cgi ###
