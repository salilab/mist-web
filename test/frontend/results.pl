#!/usr/bin/perl -w

use saliweb::Test;
use Test::More 'no_plan';
use Test::Exception;
use File::Temp qw(tempdir);

BEGIN {
    use_ok('mist');
    use_ok('saliweb::frontend');
}

my $t = new saliweb::Test('mist');

# Check results page

# Check display_ok_job
{
    my $frontend = $t->make_frontend();
    my $job = new saliweb::frontend::CompletedJob($frontend,
                        {name=>'testjob', passwd=>'foo', directory=>'/foo/bar',
                         archive_time=>'2009-01-01 08:45:00'});
    my $ret = $frontend->display_ok_job($frontend->{CGI}, $job); 
    like($ret, '/Job.*testjob.*has completed.*' .
               'Download.*MiST output/ms', 'display_ok_job');
}

# Check display_failed_job
{
    my $frontend = $t->make_frontend();
    my $job = new saliweb::frontend::CompletedJob($frontend,
                        {name=>'testjob', passwd=>'foo', directory=>'/foo/bar',
                         archive_time=>'2009-01-01 08:45:00'});
    my $ret = $frontend->display_failed_job($frontend->{CGI}, $job); 
    like($ret, '/Your MiST job.*testjob.*failed to produce any ranking.*' .
               'please see the.*#errors.*help page.*For more information, ' .
               'you can.*framework\.log.*download the MiST file-check.*' .
               'contact us/ms',
         'display_failed_job');
}

# Check get_results_page
{
    my $frontend = $t->make_frontend();
    my $job = new saliweb::frontend::CompletedJob($frontend,
                        {name=>'testjob', passwd=>'foo', directory=>'/foo/bar',
                         archive_time=>'2009-01-01 08:45:00'});
    my $tmpdir = tempdir(CLEANUP=>1);
    ok(chdir($tmpdir), "chdir into tempdir");

    my $ret = $frontend->get_results_page($job);
    like($ret, '/Your MiST job.*testjob.*failed to produce any ranking/',
         'get_results_page (failed job)');

    ok(open(FH, "> MistOutput.txt"), "Open MistOutput.txt");
    ok(close(FH), "Close MistOutput.txt");

    $ret = $frontend->get_results_page($job);
    like($ret, '/Job.*testjob.*has completed/',
         '                 (successful job)');

    chdir("/");
}
