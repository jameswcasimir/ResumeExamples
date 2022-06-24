#!/bin/bash

TZ=":America/Chicago" date

export PYTHONPATH=${PYTHONPATH}:"/scripts"

script_start_time=`date +%s` #for script timing



displaytime () {
  T="$1"
  D=$(($T/60/60/24))
  H=$(($T/60/60%24))
  M=$(($T/60%60))
  S=$(($T%60))


  (( $D > 0 )) && printf '%d days ' $D
  (( $H > 0 )) && printf '%d hours ' $H
  (( $M > 0 )) && printf '%d minutes ' $M
  (( $D > 0 || $H > 0 || $M > 0 )) && printf 'and '
  printf '%d seconds\n' $S
}



case "$1" in
  # Yak API
  -yak_api) python3 /scripts/tasks/YakAPI.py ;;

  # Ra Values
  -update_banking) python3 ./scripts/Banking/updateBankVals.py ;;
  -update_tautulli) python3 /scripts/tasks/UpdateTautulliLogs.py ;;

  # Media Manegement
  -delete_duplicate_movies) python3 /scripts/Agora/Radarr/find_duplicate_movies.py ;;
  -delete_duplicate_movies_user_input) python3 /scripts/Agora/Radarr/find_duplicate_movies_user_input.py ;;
  -unmonitor_quality_movies) python3 /scripts/Agora/Radarr/unmonitor_quality_movies.py ;;
  -search_missing_movies) python3 /scripts/Agora/Radarr/search_missing_movies.py ;;
  -add_upcoming_movies) python3 /scripts/Agora/Radarr/add_upcoming_movies.py ;;
  -fix_metadata_titles) python3 /scripts/Agora/Plex/fix_metadata_titles.py ;;


  #Download Manegment
  -pausedownloader_withPlexActivity) python3 /scripts/Agora/Tautulli/pauseDownloader_WithPlexActivity.py ;;
  -reload_nzbget) python3 /scripts/tasks/ReloadNzbGet.py ;;
  -unstickify_nzbget) python3 /scripts/Agora/NzbGet/unstickify_nzbget.py ;;
  -clear_out_failed_videos) python3 /scripts/Agora/NzbGet/clear_out_failed_videos.py ;;
  -check_provider_status) python3 /scripts/Agora/NzbGet/checkProviderStatus.py ;;
  -unpause_downloads) python3 /scripts/Agora/NzbGet/unpause_downloads.py ;;


  # Alarm
  -alarm) sh /scripts/tasks/Alarm.sh ;;

  # Webscraper
  -webscraper) python3 /scripts/tasks/WebScraper.py ;;

  # System
  -update_system) sh /scripts/tasks/UpdateSystem.sh ;;
  -set_scripts_permissions) sh /scripts/tasks/ScriptsPermissions.sh ;;
  -sync_bashrc) sh /scripts/tasks/SyncBashrc.sh ;;


  # Money
  -send_money_report) python3 /scripts/Banking/Reporting/sendMoneyReport.py ;;
  -pay_spendsave_accounts) python3 /scripts/Banking/Yakshak/paySpendsaveAccounts.py ;;

  -check_rent_balance) python3 /scripts/Webscraper/Bills/checkRentBalance.py ;;
  -make_rent_report) python3 /scripts/Webscraper/Bills/makeRentReport.py ;;


  #test
  -test_notifications) python3 /scripts/Notifications/notifier.py ;;
  -test_logging) echo "Test";;
  -count_down_days) python3 /scripts/Notifications/daycountdown.py ;;
  *) echo "Thats not a function, silly." ;;
esac


#generates human readable runtime
#return "15 seconds" or "2 hours 10 minutes 5 seconds"
script_end_time=`date +%s`
#script_runtime=$( echo "$script_end_time - $script_start_time" | bc -l | xargs printf "%.2f")
script_runtime=$( echo "$script_end_time - $script_start_time" | bc -l )


script_runtime_text=$(displaytime $script_runtime)
echo "Script finished in" $script_runtime_text

