#!/usr/bin/perl


use strict;
use warnings;
use WWW::Mechanize;
use LWP;
use JSON;
use Data::Dumper;
use Getopt::Long;
use POSIX qw/ strftime /;
my $username = 'your linkedin id';
my $password = 'yourpassword';
my $maiurl= 'https://www.linkedin.com';
my $loginurl=  $maiurl.'/uas/login?goback=&trk=hb_signin';
my $all_data = 'https://www.linkedin.com/contacts/api/contacts/?fields=id%2Cname&sort=-last_interaction';
my $json_file = '/tmp/json.data';
my $link_DB = '/opt/link.DB';



my $mech = login_linkedin();

# first hashout 2) then hashout 1)   

my $jdata = get_jdata($mech,$all_data);write_to_file($jdata,$json_file);exit;  # 1 ) get the json data and puts to /tmp/json.data  
                                                                               # OR
#my $jdata = read_from_file($json_file);                                        # 2 )  reads from json data /tmp/json.data    
 
my @contacts = gen_url ($jdata);


my $stored_id = stored_id($link_DB);




foreach (reverse @contacts){

my ($id) = $_ =~ /https:\/\/www.linkedin.com\/contacts\/api\/contacts\/(.*)\/\?fields=name,emails_extended,birthday,phone_numbers,sites,addresses,company,title,location,ims,profiles,twitter,wechat,display_sources/  ;


if ( $stored_id->{$id} ){ 

print "$id exist \n";
next;
} 

my $fnd_details_json = get_jdata($mech,$_);
my $email = $fnd_details_json->{'contact_data'}->{'emails_extended'}->[0]->{'email'};
my $title = $fnd_details_json->{'contact_data'}->{'title'};
my $name = $fnd_details_json->{'contact_data'}->{'name'};
my $company = $fnd_details_json->{'contact_data'}->{'company'}->{'name'};
my $location = $fnd_details_json->{'contact_data'}->{'location'};
 
 unless ($email) { 
 print "$id|No email ID \n";
 write_database("$id|NOID\n","$link_DB");
 next ; 

 } 
sleep(3); 
print "$name|$email|$title|$company|$location\n";
write_database("$id|$name|$email|$title|$company|$location\n","$link_DB");
}



#print Dumper (\@contacts);

sub stored_id { 
#    my $id = shift;
    my $file = shift;
#
my %hash;
    open my $fh, '<', $file or die "Could not open '$file' $!\n";

    while (my $line = <$fh>) {
        chomp $line;
      my ($id,undef) = split(/\|/,$line,2);
           $hash{$id} = 1;
     
    }

return \%hash;

} 



sub gen_url { 
my $jdata= shift;
my @url ;
for my $i (@{$jdata->{'contacts'}} ){
my $uri = $maiurl.'/contacts/api/contacts/'.$i->{'id'}.'/?fields=name,emails_extended,birthday,phone_numbers,sites,addresses,company,title,location,ims,profiles,twitter,wechat,display_sources';
push (@url,  $uri );
}
return @url;
}


sub get_jdata { 
my ( $mech,$url ) =@_;
$mech -> get ("$url");
return    decode_json($mech ->content()) ;
} 


sub login_linkedin { 
my $mech = WWW::Mechanize->new();
$mech -> cookie_jar(HTTP::Cookies->new());


$mech -> get("$loginurl");
$mech -> form_id('login');
$mech -> field ('session_key' => $username);
$mech -> field ('session_password' => $password);
$mech -> click_button (value => 'Sign In');

return $mech ;

}


sub write_database { 
my $data  = shift;
my $file  = shift;
open my $fh, ">>", "$file";
print $fh "$data";
close $fh;

}








sub read_from_file {
my $file = shift; 
my $json;
 
{
  local $/; #Enable 'slurp' mode
  open my $fh, "<", "$file";
  $json = <$fh>;
  close $fh;
 }
return decode_json($json);
}

sub write_to_file {
my $data  = shift;
my $file  = shift;
open my $fh, ">", "$file";
print $fh encode_json($data);
close $fh;
}



__DATA__
$jdata_1 = $jdata_1->[1]->{'url'};
$jdata_1 =~ s/'//g;
print "$insighturl$jdata\n";
while (1){
    sleep(2);
    $mech -> get ("$insighturl$jdata_1");
    $jdata = decode_json($mech ->content());
    print "get url $insighturl$jdata_1\n";
    if ( $jdata->[3]->{'delay'} =~ /^0$/ ) {
        print "mnt url --> ".$jdata->[3]->{'url'}."\n";
        print "delay --->". $jdata->[3]->{'delay'}."\n";
        last;
    }

}
my $D_url =  $jdata->[3]->{'url'}."\n";

$mech -> get ("$D_url");
$mech->save_content( "/tmp/mysql-slow-log-$date.$$.log" );
system("sudo mv /tmp/mysql-slow-log-$date.$$.log ${fullpath}mysql-slow-log-$date.$$.log" );
print $mech->content_type()."\n";
if ($mech ->status()){
    print "created successfully ".$fullpath."mysql-slow-log-$date.$$.log\n ";
    my $msql_slow_log_q=$fullpath."mysql-slow-log-$date.$$.log";
    system("/bin/bash $ENV{WORKSPACE}/scripts/pt-query-digest.sh $region $msql_slow_log_q ");
}
=start
https://www.linkedin.com/uas/login?goback=&trk=hb_signin

form id="login"
useame name="session_key"
password name="session_password"
value="Sign In"


get all the users in jason

https://www.linkedin.com/contacts/api/contacts/?fields=id%2Cname&sort=-last_interaction


 this is step2

 /contacts/api/contacts/li_404283088/?fields=name,emails_extended,birthday,phone_numbers,sites,addresses,company,title,location,ims,profiles,twitter,wechat,display_sources&_=1427252417780
=cut

