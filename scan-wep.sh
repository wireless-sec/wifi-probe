
#################################################################################
#
#
#  扫描周围的WEP wifi
#
#
#
#################################################################################

# 先判断本地是否存在airport文件

# 死循环扫描
while true;
do
  wep_wifi_name = `/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport en0 -s | grep WEP`
  if [ $? -eq 0 ]; then
    echo "Find WEP wifi: ${wep_wifi_name}"
  else
    echo "find..."
  fi
  sleep 1
done




