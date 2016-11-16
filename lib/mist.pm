package mist;
use saliweb::frontend;

use strict;

our @ISA = "saliweb::frontend";

sub new {
    return saliweb::frontend::new(@_, "##CONFIG##");
}

sub get_navigation_links {
    my $self = shift;
    my $q = $self->cgi;
    return [
        $q->a({-href=>$self->index_url}, "Mist Home"),
        $q->a({-href=>$self->queue_url}, "Current Mist queue"),
        $q->a({-href=>$self->help_url}, "Help"),
        $q->a({-href=>$self->contact_url}, "Contact")
#       $q->a({-href=>$self->news_url}, "News"),
        ];
}

sub get_project_menu {
    my $self = shift;
    my $version = $self->version_link;
    return <<MENU;
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h4><small>Author:</small></h4><p>Peter Cimermancic</p>
<h4><small>Web Developers:</small></h4>
<p>Peter Cimermancic<br />
Elina Tjioe<br />
Ben Webb<br /></p>

<h4><small>Corresponding Authors:</small></h4>
<p>Andrej Sali
<br /> Nevan Krogan</p>
<p><i>Version $version</i></p>
MENU
}


sub get_footer {
    my $self = shift;
    my $htmlroot = $self->htmlroot;
    return <<FOOTER;
<div id="address">
<center><a href="http://www.ncbi.nlm.nih.gov/pubmed/22190034">
<b>S. Jaeger, P. Cimermancic, et al., <i>Global landscape of HIV-human protein complexes</i>, Nature (2011)</b></a>
</center>
</div>
FOOTER
}

sub get_index_page {
    my $self = shift;
    my $q = $self->cgi;

    my $greeting = <<GREETING;
<p>MiST is a computational tool for scoring of affinity purification-mass spectrometry data.
<br><br>
<b>Note:</b> We have also developed a stand-alone version of MiST in R, hosted <a href="https://github.com/kroganlab/mist">here</a> and described <a href="http://www.currentprotocols.com/WileyCDA/CPUnit/refId-bi0819.html">here</a>.
<br />&nbsp;</p>
GREETING

    my $runningModeValues = ['training', 'trained'];
    my $runningModeLabels;
    $runningModeLabels->{"training"} = "PCA Training Mode";
    $runningModeLabels->{"trained"} = "HIV Trained Mode";

    my $filteringModeValues = ['filtering', 'no_filtering'];
    my $filteringModeLabels;
    $filteringModeLabels->{"filtering"} = "Yes";
    $filteringModeLabels->{"no_filtering"} = "No";


    return "<div id=\"resulttable\">\n" .
           $q->h2({-align=>"center"},
                  "MiST: Mass Spectrometry interaction STatistics") .
           $q->start_form({-name=>"mist_form", -method=>"post",
                           -action=>$self->submit_url}) .
         
 	   $q->table(

	       $q->Tr($q->td({-colspan=>2}, $greeting)) .

	       $q->Tr($q->td("Email address (required)",
                      $self->help_link("input_file"), $q->br),
	              $q->td($q->textfield({-name=>"email",
                                            -value=>$self->email,
                                            -size=>"25"}))) .

	       $q->Tr($q->td($q->h3("Upload input file",
		      $self->help_link("input_file"), $q->br),
                      $q->td($q->filefield({-name=>"input_file"})))) .

               $q->Tr($q->td("Name your job",
                      $q->td($q->textfield({-name=>"name",
                                            -value=>"job42", -size=>"9"})))) .

	       $q->Tr($q->td("Select MiST Running Mode",
		      $self->help_link("running_mode"),
		      $q->td($q->radio_group("running_mode", $runningModeValues, "training", 0, $runningModeLabels)))) . 

	       $q->Tr($q->td("Select Singleton Filtering",
                      $self->help_link("filtering_mode"),
                      $q->td($q->radio_group("filtering_mode", $filteringModeValues, "no_filtering", 0, $filteringModeLabels)))) .


               $q->Tr($q->td({-colspan=>"2"}, "<center>" .
                      $q->input({-type=>"submit", -value=>"Process"}) .
                      $q->input({-type=>"reset", -value=>"Reset"}) .
                             "</center><p>&nbsp;</p>"))) .
           $q->end_form .
           "</div>\n";
}


sub get_submit_page {
    my $self = shift;
    my $q = $self->cgi;
    my $userInput;

    my $user_name      = $q->param('name')||"";        $userInput->{"name"} = $user_name;
    my $email          = $q->param('email')||undef;    $userInput->{"email"} = $email;
    my $runningMode    = $q->param('running_mode');    $userInput->{"running_mode"} = $runningMode;
    my $filteringMode  = $q->param('filtering_mode');  $userInput->{"filtering_mode"} = $filteringMode;
    my $inputFile      = $q->upload('input_file');     $userInput->{"input_file"} = $inputFile;

    if (!defined ($inputFile)){
        throw saliweb::frontend::InputValidationError(
                   "Please upload input table.");
    }

    my $job = $self->make_job($user_name, $email);
    my $directory = $job->directory;


    my $input_param = $directory . "/param.txt";
    open(INPARAM, "> $input_param")
       or throw saliweb::frontend::InternalError("Cannot open $input_param: $!");
    print INPARAM "$runningMode\n";
    print INPARAM "$filteringMode\n";

    close INPARAM
       or throw saliweb::frontend::InternalError("Cannot close $input_param: $!");

    # write the input
    my $output_file_name = $directory . "/input.txt";
    open(INFILE, "> $output_file_name")
       or throw saliweb::frontend::InternalError("Cannot open $output_file_name: $!");
    my $file_contents = "";
    while (<$inputFile>) {
        $file_contents .= $_;
    }
    print INFILE $file_contents;
    close INFILE
       or throw saliweb::frontend::InternalError("Cannot close $output_file_name: $!");


    #$userInput->{"directory"} = $directory;

    #submit and user output
    $job->submit();
    
    return $q->p("Your job " . $job->name . " has been submitted.") .
           $q->p("Results will be found at <a href=\"" .
                 $job->results_url . "\">this link</a>.");

}

sub get_results_page {
    my ($self, $job) = @_;
    my $q = $self->cgi;
    if (-f "MistOutput.txt"){
        return $self->display_ok_job($q, $job);
    } else{
        return $self->display_failed_job($q, $job);
    }
}

sub display_ok_job {
   my ($self, $q, $job) = @_;
   my $return= $q->p("Job '<b>" . $job->name . "</b>' has completed.");

   $return.= $q->p("<BR>Download <a href=\"" .
          $job->get_results_file_url("MistOutput.txt").("\">MiST output.</a>") );

   $return .= $job->get_results_available_time();

   return $return;
}

sub display_failed_job {
    my ($self, $q, $job) = @_;
    my $return= $q->p("Your MiST job '<b>" . $job->name .
                      "</b>' failed to produce any ranking.");
    $return.=$q->p("This is usually caused by incorrect inputs ");
               
    $return.=$q->p("For a discussion of some common input errors, please see " .
                   "the " .
                   $q->a({-href=>$self->help_url . "#errors"}, "help page") .
                   ".");
    $return.= $q->p("For more information, you can " .
                    "<a href=\"" . $job->get_results_file_url("framework.log") .
                    "\">download the MiST file-check log file</a>." .
                    "<BR>If the problem is not clear from this log, " .
                    "please <a href=\"" .
                    $self->contact_url . "\">contact us</a> for " .
                    "further assistance.");
    return $return;
}


1;
