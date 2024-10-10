# WiFi探针（WiFi Probe）

# 一、什么是WiFi Probe

## 1.1 WiFi Auto-Join

我们平时使用手机连接WiFi的时候，如果细心一些的话可能会注意到，在WiFi连接选项中，有一个”Auto-Join“的开关，中文版本一般显示为”当设备在范围内自动连接“，我们一般会把这个开关打开，这样当下次再出现在WiFi附近时，手机就会自动连接WiFi，这样不管我们是在办公室还是在家里，手机都会自动连接WiFi而无需我们每次都手动连接了，十分方便：

![image-20240724004216478](./README.assets/image-20240724004216478.png)

而方便，它是安全最大的敌人。那这个WiFi Auto-Join功能是如何实现的呢？我们的手机要连接WiFi，无非就是两种方式，要么我们的手机主动一点去寻找WiFi，要么WiFi AP主动一点去寻找附近的手机问它要不要连我啊，而又因为无线通信不像有线通信那样可以插一根网线把信号都约束在网线内，无线通信只能广播扯着嗓子对所有人喊，WiFi AP在空气中向所有人通知自己这个AP存在，这种通信包叫做Beacon帧，这种帧不在我们本次的讨论范围内，而我们比较关注的是手机扯着嗓子喊的信号，这种信号称之为WiFi Probe，其实就是一个通信帧，这个通信帧内携带了手机的Mac地址、曾经连接过的WiFi的名称，所以会有一些数据泄露的问题，而基于这些泄露的数据就可以构建出一些攻击利用方式。





## 利用WiFi Probe获客推广（危！）

本部分介绍如何利用WiFi Probe实现获客。



需要结合Mac地址到手机号的社工库，来把抓包抓到的Mac地址对应到手机号，在app合规政策出来之前，app采集上报的信息范围是很大的，比如很多app都会上报设备的Mac地址和手机号，尤其是一些三方SDK，这些上报上去的数据可能会产生泄露（甚至是认为贩卖），通过这份数据就可以实现从Mac地址到手机号的映射，然后再通过手机号实现。





## 利用WiFi Probe抓包附近设备连接过的WiFi名称

比如下图Wireshark流量里这个名为liberty-city的SSID，是笔者的台式机上的WiFi开机卡在探测它曾经连接过的WiFi，几年前在北京的时候这块板子连接的就是liberty-city这个WiFi，时过境迁已经好久没有用过这块板子几乎忘记了它的存在，而今晚在杭州再次抓包在WiFi Probe包中看到了这个名字还愣了半天才想明白是怎么回事，还挺有意思的：

![image-20240724015420965](./README.assets/image-20240724015420965.png)







## 1.1 wifi probe的应用场景

WiFi Probe技术可以用于客流统计、位置服务和精准营销。通过分析Probe Request帧，商家可以了解顾客的行为和偏好，注意，这种行为是违法的。

我们可能有过类似的经历，在大街上走路，只是经过了一家店，过了不久就收到了这家店的营销短信，这种一般就是使用WiFi Probe技术实现的。

![How to Log Wi-Fi Probe Requests from Smartphones & Laptops with ...](./README.assets/log-wi-fi-probe-requests-from-smartphones-laptops-with-probemon.w1456.jpg)

## 1.2 WiFi Probe技术实现

WiFi Probe是一种无线网络扫描技术，用于发现和识别周围的无线网络。这种技术主要涉及两种类型的帧：Probe Request帧和Probe Response帧。以下是WiFi Probe的一些关键点：

1. **Probe Request帧**：
   - 设备（如智能手机、笔记本电脑等）发送Probe Request帧来主动探测周围的无线网络。这些帧可以包含特定的SSID（服务集标识符），或者是一个空的SSID字段（Wildcard SSID），甚至不包含SSID字段。
2. **Probe Response帧**：
   - 当接入点（AP）接收到Probe Request帧时，如果SSID匹配或帧是广播的，则AP会发送Probe Response帧作为响应。Probe Response帧包含了AP的详细信息，如SSID、支持的速率、安全协议等。
3. **主动扫描**：
   - WiFi Probe通常在主动扫描过程中使用。设备通过发送Probe Request帧并监听Probe Response帧来发现周围的无线网络。
4. **被动扫描**：
   - 与主动扫描相对的是被动扫描，设备通过监听AP定期发送的Beacon帧来发现网络。被动扫描不需要设备发送任何帧，因此能耗较低。
5. **SSID发现**：
   - 在Probe Request帧中，设备可以指定一个SSID，这样只有支持该SSID的AP会响应。如果SSID字段为空或包含通配符，则所有在范围内的AP都会响应。
6. **网络选择**：
   - 设备使用Probe Request和Probe Response帧来评估周围的无线网络，并选择一个合适的网络进行连接。这通常基于信号强度、支持的速率、安全协议等因素。
7. **隐私和安全**：
   - 一些设备可能会使用随机化的MAC地址发送Probe Request帧，以提高隐私保护和防止被跟踪。

总结来说，WiFi Probe是一种有效的无线网络发现机制，它允许设备主动或被动地发现并评估周围的无线网络，从而做出连接决策。





# 二、Probe Request帧

Probe Request帧是无线设备用来探测附近的热点的，可以包含

```bash
wlan.fc.type_subtype == 0x04
```



![image-20240723223824908](./README.assets/image-20240723223824908.png)



## Type/Subtype

- Probe Request帧的类型和子类型为0x04

![image-20240723225650405](./README.assets/image-20240723225650405.png)



## Frame Control Field



![image-20240723225803332](./README.assets/image-20240723225803332.png)

## Duration

Duration表示wifi设备在发送出wifi probe请求包之后，会保持监听多长时间来接收probe response响应包，这个值的单位是微秒。

在主动扫描过程中，设备发送Probe Request帧以发现周围的无线网络。Probe Request帧的Duration字段通常设置为0，因为这些帧不需要AP进行响应，因此不保留无线介质。

Duration字段的值可以是固定的，也可以是动态计算的。在某些情况下，设备会根据当前的网络条件和设备状态动态调整Duration字段的值。

![image-20240723225834163](./README.assets/image-20240723225834163.png)

## Receiver Address

Receiver Address用于设置这个帧是发送给是的，通常设置为广播地址（ff:ff:ff:ff:ff:ff），以便所有在范围内的接入点（AP）都能接收到。

Probe Request帧是主动扫描的一部分。设备通过发送目的地址为广播地址的Probe Request帧来主动发现周围的无线网络。这种帧包含设备希望连接的网络的SSID（如果有指定的话）或其他扫描参数。

当AP接收到Probe Request帧时，如果SSID匹配或帧是广播的，则AP会发送Probe Response帧作为响应。Probe Response帧包含了AP的详细信息，如SSID、支持的速率、安全协议等。

在主动扫描过程中，设备会在每个信道上发送Probe Request帧，并等待AP的响应。这个过程有助于设备了解周围可用的无线网络，并选择一个合适的网络进行连接。

![image-20240723225906352](./README.assets/image-20240723225906352.png)

## Destinaton address

在Probe Request帧中，目的地址字段通常设置为广播地址（ff:ff:ff:ff:ff:ff）。这意味着这个帧是发送给所有在范围内的接入点（AP）的。

Probe Request帧是主动扫描的一部分。设备通过发送目的地址为广播地址的Probe Request帧来主动发现周围的无线网络。这种帧包含设备希望连接的网络的SSID（如果有指定的话）或其他扫描参数。

当AP接收到Probe Request帧时，如果SSID匹配或帧是广播的，则AP会发送Probe Response帧作为响应。Probe Response帧包含了AP的详细信息，如SSID、支持的速率、安全协议等。

在主动扫描过程中，设备会在每个信道上发送Probe Request帧，并等待AP的响应。这个过程有助于设备了解周围可用的无线网络，并选择一个合适的网络进行连接。

![image-20240723230004109](./README.assets/image-20240723230004109.png)

## Transmitter Address

"Transmitter Address"字段包含发送Probe Request帧的设备的物理MAC地址。这个地址在帧中用于标识发送设备的网络设备。

![image-20240723230718815](./README.assets/image-20240723230718815.png)

这个wifi probe帧的Transmitter Address地址是78:11:dc:77:d2:4a：

![image-20240723230056444](./README.assets/image-20240723230056444.png)

需要注意的是设备的Mac地址可能会暴漏生产厂商的信息，比如这个Mac地址

```
78:11:dc:77:d2:4a
```

选择一个在线查询Mac地址，发现这个Mac地址对应着一个小米的设备：

![image-20240723230927251](./README.assets/image-20240723230927251.png)

## Source Address

源地址

![image-20240723230114516](./README.assets/image-20240723230114516.png)



## BSS ID

在Probe Request帧中，BSS ID字段可以被用来指定设备希望连接的特定网络。设备可以通过发送包含特定SSID的Probe Request帧来请求只有支持该SSID的AP响应。

![image-20240723230131857](./README.assets/image-20240723230131857.png)

## Fragment number

![image-20240723230220656](./README.assets/image-20240723230220656.png)

![image-20240723230432252](./README.assets/image-20240723230432252.png)

## Sequence number



![image-20240723230246820](./README.assets/image-20240723230246820.png)

![image-20240723230417231](./README.assets/image-20240723230417231.png)





## Frame check sequence 

![image-20240723230306826](./README.assets/image-20240723230306826.png)

![image-20240723230359076](./README.assets/image-20240723230359076.png)



## FCS Status

![image-20240723230327381](./README.assets/image-20240723230327381.png)



## WLAN Flags



![image-20240723230339147](./README.assets/image-20240723230339147.png)





# 三、Probe Response帧

Wireshark筛选出Probe Response帧：

```
wlan.fc.type_subtype == 0x05
```



![image-20240723224416684](./README.assets/image-20240723224416684.png)





![image-20240724005627823](./README.assets/image-20240724005627823.png)

## Type/Subtype

![image-20240724005648137](./README.assets/image-20240724005648137.png)

## Frame Control Field

![image-20240724005726499](./README.assets/image-20240724005726499.png)

## Duration

![image-20240724005755177](./README.assets/image-20240724005755177.png)

## Receiver address

![image-20240724005815143](./README.assets/image-20240724005815143.png)

## Destinaton address

![image-20240724005837964](./README.assets/image-20240724005837964.png)

## Transmitter address

![image-20240724005854699](./README.assets/image-20240724005854699.png)

## Source address

![image-20240724005916653](./README.assets/image-20240724005916653.png)

## BSS ID

![image-20240724005934183](./README.assets/image-20240724005934183.png)

## Fragment number

![image-20240724005949456](./README.assets/image-20240724005949456.png)

## Sequence number

![image-20240724010004961](./README.assets/image-20240724010004961.png)



![image-20240724010024470](./README.assets/image-20240724010024470.png)



![image-20240724010037221](./README.assets/image-20240724010037221.png)



![image-20240724010047620](./README.assets/image-20240724010047620.png)











# 四、Mac地址随机化

## 什么是Mac地址随机化？

当我们把手机携带在身上的时候，手机时时刻刻都会在空气中广播发送一堆包，几乎像三体人一样透明，Mac地址随机化的思路就是广播还是继续广播，但是每隔一段时间就会切换一下Mac地址，让抓包的人无法定位自己，以此来实现”隐身“。

通过使用随机化的MAC地址，设备可以隐藏其真实的物理地址，防止被跟踪和识别。这对于保护用户隐私和防止设备被恶意识别非常有用。

在WiFi Probe Request帧中，设备可以使用随机化的MAC地址来发送帧，以便在发现网络时不暴露其真实身份。这有助于防止未授权的网络扫描和设备识别。

WiFi Probe的MAC地址随机化是一种技术，它允许设备在发送Probe Request帧时使用随机生成的MAC地址，而不是其实际的物理MAC地址。这种技术主要用于提高隐私保护和安全性。以下是一些关键点：

1. **隐私保护**：
   - 通过使用随机化的MAC地址，设备可以隐藏其真实的物理地址，防止被跟踪和识别。这对于保护用户隐私和防止设备被恶意识别非常有用。

2. **安全性**：
   - 随机化的MAC地址可以减少设备被攻击的风险。攻击者难以通过MAC地址来识别和攻击特定的设备，因为这些地址是随机生成的，并且每次通信都可能不同。

3. **网络发现**：
   - 在WiFi Probe过程中，设备通过发送Probe Request帧来主动发现周围的无线网络。这些帧可以包含特定的SSID，或者是一个空的SSID字段（Wildcard SSID），甚至不包含SSID字段。使用随机化的MAC地址可以防止设备的真实身份被轻易识别。

4. **设备行为分析**：
   - 通过分析设备发送的Probe Request帧的内容和频率，可以识别出设备是否在使用随机化的MAC地址。例如，某些设备在发送Probe Request帧时可能会使用随机化的MAC地址。

5. **统计分析**：
   - 通过统计分析随机化MAC地址的出现频率和分布，可以识别出设备是否在使用随机化的MAC地址。这种方法需要大量的数据和复杂的算法来实现。

6. **设备配置和设置**：
   - 在某些操作系统中，可以通过检查设备的配置和设置来确定是否启用了MAC地址随机化功能。例如，在Android系统中，可以通过设置界面中的选项来启用或禁用随机化MAC地址。

7. **网络设备识别**：
   - 网络设备和接入点可以通过检查连接请求中的MAC地址是否符合随机化的特征来识别设备是否在使用随机化的MAC地址。这种方法需要设备和网络设备之间的协同工作。

8. **实验和测试**：
   - 通过在受控环境中进行实验和测试，可以验证随机化MAC地址的效果和识别方法的有效性。例如，通过在城市环境中进行测试，可以评估随机化MAC地址在实际应用中的表现。

9. **识别方法**：
   - 识别随机化的MAC地址可以通过检查MAC地址的第一个字节的第二个最低有效位（LSB）。如果这个位是1，则表明该MAC地址是随机生成的。

通过这些方法，可以有效地识别和处理随机化MAC地址，从而在保护用户隐私的同时，确保网络的正常运行和安全性。

## 如何破解Mac地址随机化？

1. **本地管理位（Locally Administered Address, LAA）**：
   - 随机化的MAC地址通常会将本地管理位设置为1，而单播位设置为0。本地管理位位于MAC地址的第一个字节的第二个最低有效位（LSB）。如果这个位是1，则表明该MAC地址是随机生成的。

2. **随机化特征**：
   - 随机化的MAC地址具有一些特征，可以通过分析这些特征来识别。例如，随机化的MAC地址可能会在某些字段中包含特定的模式或值。

3. **设备行为分析**：
   - 通过分析设备发送的Probe Request帧的内容和频率，可以识别出设备是否在使用随机化的MAC地址。例如，某些设备在发送Probe Request帧时可能会使用随机化的MAC地址。

4. **统计分析**：
   - 通过统计分析随机化MAC地址的出现频率和分布，可以识别出设备是否在使用随机化的MAC地址。这种方法需要大量的数据和复杂的算法来实现。

5. **设备配置和设置**：
   - 在某些操作系统中，可以通过检查设备的配置和设置来确定是否启用了MAC地址随机化功能。例如，在Android系统中，可以通过设置界面中的选项来启用或禁用随机化MAC地址。

6. **网络设备识别**：
   - 网络设备和接入点可以通过检查连接请求中的MAC地址是否符合随机化的特征来识别设备是否在使用随机化的MAC地址。这种方法需要设备和网络设备之间的协同工作。

7. **实验和测试**：
   - 通过在受控环境中进行实验和测试，可以验证随机化MAC地址的效果和识别方法的有效性。例如，通过在城市环境中进行测试，可以评估随机化MAC地址在实际应用中的表现。

# 五、Rogue APs攻击





