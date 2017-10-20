#!/usr/bin/perl -w

use saliweb::Test;
use saliweb::frontend;
use Test::More 'no_plan';
use Test::Exception;
use File::Temp;

BEGIN {
    use_ok('mist');
}

my $t = new saliweb::Test('mist');

# Check job submission

# Check get_submit_page
{
    my $self = $t->make_frontend();
    my $cgi = $self->cgi;

    my $tmpdir = File::Temp::tempdir(CLEANUP=>1);
    ok(chdir($tmpdir), "chdir into tempdir");
    ok(mkdir("incoming"), "mkdir incoming");

    throws_ok { $self->get_submit_page() }
              saliweb::frontend::InputValidationError,
              "no input table";

    ok(open(FH, "> foo"), "Open foo");
    print FH "input\n";
    ok(close(FH), "Close foo");
    open(FH, "foo");


    $cgi->param('input_file', \*FH);
    $cgi->param('name', 'test');
    $cgi->param('filtering_mode', 'filtering');
    $cgi->param('running_mode', 'training');
    my $ret = $self->get_submit_page();
    like($ret, qr/Your job.*has been submitted.*Results will be found at/ms,
         "submit page HTML");

    chdir('/') # Allow the temporary directory to be deleted
}
