#
# Cookbook Name:: local
# Recipe:: redis
#
# Finish setting up the Redis server.
#
# Copyright 2015, Kevin Cureton
#

# Define the base log directory and setup each server to log
# in that location.
#
redis_log_dir = "/var/log/redis"

directory "#{redis_log_dir}" do
    mode "0755"
    owner "redis"
    group "redis"
    action :create
    not_if { File.exists?("#{redis_log_dir}") }
end

# Make modifications to the Redis server setups
#
redis_instances = node['local']['redis']['servers']
redis_instances.each do |current_server|
    node.set.current_server['logfile'] = "#{redis_log_dir}/#{current_server['name']}.log"
    node.set.current_server['syslogenabled'] = "no"
end

# Set the appropriate attributes for the 'redisio' cookbook.
node.set['redisio']['servers'] = redis_instances

# Install redis using the 'redisio' cookbook.
include_recipe "redisio"
include_recipe "redisio::enable"
