from pywifi import PyWiFi, const
from scapy.all import *
from scapy.layers.dot11 import Dot11ProbeReq, Dot11Elt


def handle_packet(packet):
    if packet.haslayer(Dot11ProbeReq):
        ssid = packet[Dot11Elt].info.decode()
        print(f"捕获到 Probe Request: SSID={ssid}")


wifi = PyWiFi()
iface = wifi.interfaces()[0]  # 获取第一个 Wi-Fi 接口
if iface.status() == const.IFACE_CONNECTED:
    iface.disconnect()
monitor_conf = iface.add_monitor_network(const.PHY_MODE_80211B | const.PHY_MODE_80211G | const.PHY_MODE_80211A)
iface.down()
iface.up()
if iface.status() == const.IFACE_DOWN:
    print("Interface is down.")
elif iface.status() == const.IFACE_MONITOR:
    print("Interface is in monitor mode.")

sniff(prn=handle_packet, iface="en0")  # 请根据你的无线接口修改
