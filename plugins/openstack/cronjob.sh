#!/bin/bash

# Copyright (C) 2017   Robin Cernin (rcernin@redhat.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Checking cronjob
# Ref: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/8/html-single/director_installation_and_usage/#sect-Tuning_the_Undercloud 
REFNAME="Cronjob module"

function cronjob_check_live(){
   continue
}

function cronjob_check_sosreport(){

  # Crontab check
  grep_file "${DIRECTORY}/var/spool/cron/keystone" "keystone-manage token_flush"
  grep_file "${DIRECTORY}/var/spool/cron/heat" "heat-manage purge_deleted"

}

# Cluster module
cronjob_check_${CHECK_MODE}


