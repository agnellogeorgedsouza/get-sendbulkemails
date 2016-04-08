#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use LWP::Simple;

my $url = 'http://www.cybercoders.com/recruiter/';



my $html =  get "$url";

my @html = split(/\n/,$html);

for my $i  (@html){
    next unless  $i =~ /<a href="\/recruiter\/(\S.*\/)">/ ;
#    print "${url}${1}\n";
    my $indiv_recruiter = get("$url$1");
    my @indiv_recruiter = split(/\n/,$indiv_recruiter);
    for my $j (@indiv_recruiter ){

     next unless $j =~ /<a class="recruiter-email-link" href="mailto:(\S.*?\@CyberCoders\.com)">/ ;
        print "$1\n"

    }
}

