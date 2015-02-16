#
# Cookbook Name:: local
# Recipe:: httpd
#
# Copyright 2015, Kevin Cureton
#

template "/etc/httpd/conf-available/local.conf" do
    source "etc/httpd/conf-available/local.conf.erb"
    mode "644"
    owner "root"
    group "root"
end

link "/etc/httpd/conf-enabled/local.conf" do
    to "/etc/httpd/conf-available/local.conf"
    action :create
end

template "/etc/httpd/ssl/apache.crt" do
    source "etc/httpd/ssl/apache.crt"
    mode "644"
    owner "root"
    group "root"
end

template "/etc/httpd/ssl/apache.key" do
    source "etc/httpd/ssl/apache.key"
    mode "644"
    owner "root"
    group "root"
end
