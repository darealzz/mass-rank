from datetime import datetime
import requests
import sys

cookie = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_446FC9DDF137D6D7B9296D70CF8D466894C7453EEE63B65B5BEB66985EE27278F8598310D834CCA43ECEB0072B0511F01DA3A651783785D335EF43B14C66ADA8CDDCEA68CA4BCD44EDA3D722A1D6D758B5915C913F625D481802EFD3D8998722352A60C188CB352854196EA1D1065B4F0641AF391B22BD533F45834D1283DA723116B3048C7464FC72710178D9245A05644211FFDF0C64342A6B9C0AAF10B79C709FF3BB6B4444AED4A4958F2A01DF462F7799EB2D5E3E73B3240F5C2A2EA3A0C9998B284CF9D34766F6671C5427BC1387DE4B3978D12479301D833E701548DFAB13E06F481D31AADB4F2E3EC8575C36AB788ADF16A41470694DDD11FD696E4AEAE568930179A6EF423C4942C1425F0152C7645820FCF24F47120B4E8B20594CB7A0377E8484C504DDECDFC773F2D5EB921DA461ED8D2F39BA1232960F6AC63548B88DF89E74E2C3DEEF7497E7670D640551030E'

while True:
    ct = datetime.now().strftime('%H')
    if ct == 6:

        cookies = {
            '.ROBLOSECURITY': cookie
        }
        request = requests.patch('https://groups.roblox.com/v1/groups/6760741/users/1079054514', 
        cookies={'.ROBLOSECURITY': cookie}, 
        data={'roleId': 43160349},
        headers={'X-CSRF-TOKEN': requests.post(url=f'https://auth.roblox.com/v1/logout', cookies=cookies).headers['x-csrf-token']}
        )
        print('[+] Ranked the guy')
        print(f'[+] {ct}')
        break