#!/usr/bin/perl -w
#
# clamshellstate.pl
#
my $PgmName = "clamshellstate - Get state of the clamshell";
my $VERSION = "0.1e, 30-Nov-2012";
#

=head1 clamshellstate

 This program has been written just for fun to determine the state
  of the clamshell/lib (Open|Closed|Undetermined|Not present)
  of a Mac OS X machine.

 Revision history: 
   V0.1e,  2012-Nov-30, improved error handling
   V0.1d,  2012-Nov-30, improved error handling
   V0.1c,  2012-Nov-30, improved comments and error handling
   V0.1b,  2012-Nov-30, improved arguments & diagnostics
   V0.1a,  2012-Nov-30, first version

 usage: perl clamshellstate.pl [VERB]
    VERB = 0 no output.  Exit/return status only.
    VERB = 1 brief output: Open|Closed|Undetermined|Not present


From IOPM.h
/* AppleClamshellState 
 * reflects the state of the clamshell (lid) on a portable.
 * It has a boolean value.
 *  true        == clamshell is closed (1, Yes)
 *  false       == clamshell is open   (0, No)
 *  not present == no clamshell on this hardware
 */

A typical output from:
  $ioreg -r -k AppleClamshellState -d 4 | grep AppleClamshellState  | head -1
is:
    |   "AppleClamshellState" = No

=cut 

use strict;
use IO::Socket;
use Time::HiRes qw(time);
use Getopt::Long;
use Sys::Hostname;
  
sub usage { # print a short 'usage' message and exit
my @exc = split('/',$0);
  print "usage: perl $exc[-1] \n";
  print "              [--verb=VERB]\n";
  print "              [-v VERB]\n";
  print "                 [0 no output.  Only return status.  Default.]\n";
  print "                 [1 clamshell state: open | closed.]\n";
  print "              [--diag=DIAG]\n";
  print "              [-d DIAG]\n";
  print "                 [0 no diagnostic output.  Default.]\n";
  print "                 [1 minimum diagnostic output.]\n";
  print "                 [9 maximum diagnostic output.]\n";
  print " Exit/Return status: \n";
  print "   0 = clamshell is open. \n";
  print "   1 = clamshell is closed. \n";
  print " 255 = clamshell state is undetermined. \n";
  print " 254 = clamshell isn't present. \n";
  print " 253 = ioreg didn't execute properly. \n";
#
  exit 255; # Usage.
}

sub clopen {
    if ( $_[0] == 1 ) { print "Open\n"; }
    if ( $_[0] > 1 ) { print "The state of the clamshell is: Open\n"; }
    exit 0;
}

sub clclosed {
    if ( $_[0] == 1 ) { print "Closed\n"; }
    if ( $_[0] > 1 ) { print "The state of the clamshell is: Closed\n"; }
    exit 1;
}

sub clundetermined {
    if ( $_[0] == 1) { print "Undetermined\n"; }
    if ( $_[0] > 1 ) { print "The state of the clamshell is: Undetermined\n"; }
    exit 254;
}

sub clnotpresent {
    if ( $_[0] == 1 ) { print "Not present\n"; }
    if ( $_[0] > 1 ) { print "There is no clamshell on this machine.\n"; }
    exit 255;
}

use vars qw($opt_h $opt_v $opt_d); # command line options

my $diag = 0;
my $verb = 0;
my @exc = split('/',$0);

# handle the commandline options
#  getopts('hud');           # look for -h, -u and -d with an argument
GetOptions ('verb|v=i' => \$opt_v, 'diag|d=i' => \$opt_d, 'help|h|?' => \$opt_h);
  $opt_h && usage;          # -h print usage message and exit
  if ( $opt_d ) {
      $diag = $opt_d;
      if ( $diag > 0 ) {print "diag: $diag \n";}
  } else { $diag = 0; }
  if ( $opt_v ) {
      $verb = $opt_v;
      if ( $diag > 0 ) {print "verb: $verb \n";}
  } else { $verb = 0; }
  if ( $verb > 1 ) {
     print "$exc[-1] \n";
     print " $PgmName \n";
     print "  V $VERSION \n";
  }
  if (!$ARGV[0]) {
# There are no arguments.  Do nothing, continue.
    } elsif ($ARGV[0] !~ "[^0-9]" ) {
        $verb = $ARGV[0];
        if ( $verb < 0 ) {$verb = 0;}
        if ( $verb > 9 ) {$verb = 9;}
        if ( $diag > 0 ) {print "verb: $verb \n";}
    } else {
# There is an argument, but it isn't an integer.  Do nothing, continue.
  }

  my $ioreg = "/usr/sbin/ioreg";
  my $key = "AppleClamshellState";
  my $class = "IOPMrootDomain";
  my $statestring = "";
  my $statestringlen = 0;
  my $keypos = 0;
  my $state = "";
  my $eqpos = 0;

  # main *********************************************************************

# Run ioreg and sort through the output line by line.
# $statestring = `$ioreg -k $key -d 4 | grep $key | head -1`;
open(IOR,"$ioreg -r -k $key -d 4 |") || exit 253;
# Find the first string that matches $key.
while ( <IOR> )
{
    if (/$key/) {
	if ( $diag > 1 ) { print $_; }
	$statestring = $_;
	chomp $statestring;
	if ( $diag > 0 ) { print "statestring: $statestring \n"; }
	last;
    }
}
# If nothing matches $key, then the machine doesn't have a clamshell/lid.
if ( $diag > 0 ) { 
    print "statestring length: " . sprintf("%i",length($statestring)) . "\n";
}
if ( length($statestring) == 0 ) { clnotpresent($verb); }

# Find the location of the $key in the string.
$keypos = index($statestring,$key);
if ( $diag > 0 ) { print "keypos: $keypos \n"; }

# If there is no $key substring, something is weird.  Exit.
if ( $keypos == -1 ) { clundetermined($verb); }

# Find the location of the " = " in the string.
$eqpos = index($statestring, " = ");
if ( $diag > 0 ) { print "eqpos: $eqpos \n"; }

# If there is no " = " substring, something is weird.  Exit.
if ( $eqpos == -1 ) { clundetermined($verb); }

# Test to be sure the location of " = " is after $key in the string.
# If not, something is wierd.  Exit.
if ( $eqpos < $keypos ) { clundetermined($verb); }

# Get the substring after " = "
$state = substr($statestring, $eqpos+3);
if ( $diag > 0 ) { print "state: $state \n"; }

# If the length of the substring after " = " is zero, something is weird.  Exit.
if ( $diag > 0 ) { 
    print "substring length: " . sprintf("%i",length($state)) . "\n";
}
if ( length($state) == 0 ) { clundetermined($verb); }

# If the substring after " = " contains No, then the clamshell is open.
if ( $state =~ /No/ ) { clopen($verb); }

# If the substring after " = " contains Yes, then the clamshell is closed.
if ( $state =~ /Yes/ ) { clclosed($verb); }

# If the substring after " = " contains neither Yes nor No, then 
#   something is wierd.  Exit
clundetermined($verb);

__END__