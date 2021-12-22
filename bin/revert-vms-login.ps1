#!/usr/bin/env pwsh

param
(
	[Parameter(Mandatory, HelpMessage = "Provide connection information to the ESXI host")]
	$server,
	[Parameter(Mandatory, HelpMessage = "Username required")]
	$user,
	[Parameter(Mandatory, HelpMessage = "Password required")]
	$passwd,
	[Parameter(Mandatory, HelpMessage = "Lab to perform the operation on")]
	$lab
)

function Connect-ToESXI {
	param (
		$ip,
		$user,
		$passwd
	)

	if($passwd -eq '') { # password parameter present
		# login without password
		$script:con = Connect-VIServer -Server $server -User $user -ErrorAction 
	}
	else {
		# login with password
		$script:con = Connect-VIServer -Server $server -User $user -Password $passwd
	}
	# check if connection was successful (var null or not)
	if(!$script:con)
	{
		Write-Host "Not connected" -ForegroundColor Red 
		exit
	}
}

function RevertToBaseSnapshot 
{
	param
	(
		$lab
	)
	# loop through VMs
	foreach($vm in Get-VM -Name "Lab $lab*") 
	{
		$snap = Get-Snapshot -Name "base" -VM $vm
		if ($snap) {
			Write-Host "Reverting machine $vm to snapshot $snap" -ForegroundColor Yellow
			Set-VM -VM $vm -SnapShot $snap -Confirm:$false
		}
	}
}
$script:con # scope = script
if(!$script:con) {
	Write-Host "Connection to vCenter server..."
	Connect-ToESXI -ip $esxi -user $user -passwd $passwd
	Write-Host "Connected" -ForegroundColor Green
}
else {
	Write-Host "Already connected" -ForegroundColor Green
}

# Revert machines for lab $lab to the base snapshot
RevertToBaseSnapshot -lab $lab

Write-Host "Operation finished." -ForegroundColor Green