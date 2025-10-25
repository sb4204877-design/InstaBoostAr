try:
    from requests.exceptions import RequestException
    import requests, re, json, time, os, sys
    from rich.console import Console
    from rich.panel import Panel
    from rich import print as printf
    from requests.exceptions import SSLError
except (ModuleNotFoundError) as e:
    __import__('sys').exit(f"[خطأ] {str(e).capitalize()}!")

SUKSES, GAGAL, FOLLOWERS, STATUS, BAD, CHECKPOINT, FAILED, TRY = [], [], {
    "COUNT": 0
}, [], [], [], [], []

class KIRIMKAN:

    def __init__(self) -> None:
        pass

    def PENGIKUT(self, session, username, password, host, your_username):
        global SUKSES, GAGAL, STATUS, FAILED, BAD, CHECKPOINT
        session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Mode': 'navigate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'ar,en;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Host': '{}'.format(host),
            'Sec-Fetch-Dest': 'document',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Connection': 'keep-alive'
        })
        response = session.get('https://{}/login'.format(host))
        self.ANTI_FORGERY_TOKEN = re.search(r'"&antiForgeryToken=(.*?)";', str(response.text))
        if self.ANTI_FORGERY_TOKEN is not None:
            self.TOKEN = self.ANTI_FORGERY_TOKEN.group(1)
            session.headers.update({
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://{}/login'.format(host),
                'Sec-Fetch-Mode': 'cors',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Sec-Fetch-Dest': 'empty',
                'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()]),
                'Origin': 'https://{}'.format(host)
            })
            data = {
                'username': f'{username}',
                'antiForgeryToken': f'{self.TOKEN}',
                'userid': '',
                'password': f'{password}'
            }
            response2 = session.post('https://{}/login?'.format(host), data=data)
            self.JSON_RESPONSE = json.loads(response2.text)
            if '\'status\': \'success\'' in str(self.JSON_RESPONSE):
                session.headers.update({
                    'Referer': 'https://{}/tools/send-follower'.format(host),
                    'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                })
                data = {
                    'username': f'{your_username}',
                }
                response3 = session.post('https://{}/tools/send-follower?formType=findUserID'.format(host), data=data)
                if 'name="userID"' in str(response3.text):
                    self.USER_ID = re.search(r'name="userID" value="(\d+)">', str(response3.text)).group(1)
                    session.headers.update({
                        'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
                    })
                    data = {
                        'userName': f'{your_username}',
                        'adet': '500',
                        'userID': f'{self.USER_ID}',
                    }
                    response4 = session.post('https://{}/tools/send-follower/{}?formType=send'.format(host, self.USER_ID), data=data)
                    self.JSON_RESPONSE4 = json.loads(response4.text)
                    if '\'status\': \'success\'' in str(self.JSON_RESPONSE4):
                        SUKSES.append(f'{self.JSON_RESPONSE4}')
                        STATUS.append(f'{self.JSON_RESPONSE4}')
                    elif '\'code\': \'nocreditleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] انتهت رصيدك في الخدمة!          ", end='\r')
                        time.sleep(4.5)
                    elif '\'code\': \'nouserleft\'' in str(self.JSON_RESPONSE4):
                        printf(f"[bold bright_black]   ──>[bold red] لا يوجد مستخدمون متاحون!        ", end='\r')
                        time.sleep(4.5)
                    elif 'istek engellendi.' in str(self.JSON_RESPONSE4):
                        TRY.append(f'{self.JSON_RESPONSE4}')
                        if len(TRY) >= 3:
                            TRY.clear()
                            printf(f"[bold bright_black]   ──>[bold red] تم حظر طلب إرسال المتابعين!  ", end='\r')
                            time.sleep(4.5)
                            return False
                        else:
                            self.PENGIKUT(session, username, password, host, your_username)
                    else:
                        GAGAL.append(f'{self.JSON_RESPONSE4}')
                        printf(f"[bold bright_black]   ──>[bold red] خطأ أثناء إرسال المتابعين!      ", end='\r')
                        time.sleep(4.5)
                    printf(f"[bold bright_black]   ──>[bold green] اكتمل الإرسال من خدمة {str(host).split('.')[0].upper()}!           ", end='\r')
                    time.sleep(5.0)
                    return True
                else:
                    printf(f"[bold bright_black]   ──>[bold red] اسم المستخدم غير موجود!           ", end='\r')
                    time.sleep(4.5)
                    return False
            elif 'Güvenliksiz giriş tespit edildi.' in str(self.JSON_RESPONSE):
                CHECKPOINT.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] حسابك يحتاج تحقق أمني!          ", end='\r')
                time.sleep(4.5)
                return False
            elif 'Üzgünüz, şifren yanlıştı.' in str(self.JSON_RESPONSE):
                BAD.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] كلمة المرور غير صحيحة!              ", end='\r')
                time.sleep(4.5)
                return False
            else:
                FAILED.append(f'{self.JSON_RESPONSE}')
                printf(f"[bold bright_black]   ──>[bold red] خطأ في تسجيل الدخول!                          ", end='\r')
                time.sleep(4.5)
                return False
        else:
            printf(f"[bold bright_black]   ──>[bold red] لم يتم العثور على رمز الأمان!          ", end='\r')
            time.sleep(2.5)
            return False

class INFORMASI:

    def __init__(self) -> None:
        pass

    def PENGIKUT(self, your_username, updated):
        global FOLLOWERS
        with requests.Session() as session:
            session.headers.update({
                'User-Agent': 'Instagram 317.0.0.0.3 Android (27/8.1.0; 360dpi; 720x1280; LAVA; Z60s; Z60s; mt6739; en_IN; 559698990)',
                'Host': 'i.instagram.com',
                'Accept-Language': 'ar,en;q=0.9',
            })
            response = session.get('https://i.instagram.com/api/v1/users/web_profile_info/?username={}'.format(your_username))
            if '"status":"ok"' in str(response.text):
                self.EDGE_FOLLOWED_BY = json.loads(response.text)['data']['user']['edge_followed_by']['count']
                if bool(updated):
                    FOLLOWERS.update({
                        "COUNT": int(self.EDGE_FOLLOWED_BY)
                    })
                    return True
                else:
                    self.JUMLAH_MASUK = (int(self.EDGE_FOLLOWED_BY) - int(FOLLOWERS['COUNT']))
                    return f'+{self.JUMLAH_MASUK} > {self.EDGE_FOLLOWED_BY}'
            else:
                if bool(updated):
                    FOLLOWERS.update({
                        "COUNT": 0
                    })
                    return False
                else:
                    return '-+500'

class MAIN:

    def __init__(self):
        global CHECKPOINT, BAD, FAILED
        try:
            self.LOGO()
            printf(Panel(
                "[bold white]الرجاء إدخال بيانات حساب إنستغرام الوهمي الخاص بك (اسم المستخدم وكلمة المرور)،\n"
                "استخدم الرمز `[bold red]:[bold white]` كفاصل بينهما. تأكد من استخدام حساب وهمي!",
                width=59, style="bold bright_black",
                title="[bold bright_black]تسجيل الدخول مطلوب",
                subtitle="[bold bright_black]╭──────",
                subtitle_align="left"
            ))
            self.ACCOUNTS = Console().input("[bold bright_black]   ╰─> ")
            if ':' in str(self.ACCOUNTS):
                self.USERNAME, self.PASSWORD = self.ACCOUNTS.split(':')[0], self.ACCOUNTS.split(':')[1]
                printf(Panel(
                    "[bold white]الرجاء إدخال اسم المستخدم الخاص بحسابك الذي تريد زيادة متابعيه.\n"
                    "تأكد من أن الحساب غير مقفول. مثال: [bold green]@salah_badi",
                    width=59, style="bold bright_black",
                    title="[bold bright_black]حسابك المستهدف",
                    subtitle="[bold bright_black]╭──────",
                    subtitle_align="left"
                ))
                self.YOUR_USERNAME = Console().input("[bold bright_black]   ╰─> ").replace('@', '')
                if len(self.YOUR_USERNAME) != 0:
                    printf(Panel(
                        "[bold white]أثناء إرسال المتابعين، يمكنك استخدام [bold yellow]CTRL + C[bold white] للتوقف المؤقت،\n"
                        "و[bold red]CTRL + Z[bold white] للإيقاف الكامل. في حال حدوث خطأ، تحقق من الحساب والخدمة!",
                        width=59, style="bold bright_black",
                        title="[bold bright_black]ملاحظة مهمة"
                    ))
                    while True:
                        try:
                            INFORMASI().PENGIKUT(your_username=self.YOUR_USERNAME, updated=True)
                            CHECKPOINT.clear(); BAD.clear(); FAILED.clear()
                            for HOST in ['instamoda.org', 'takipcitime.com', 'takipcikrali.com', 'bigtakip.net', 'takipcimx.net']:
                                try:
                                    with requests.Session() as session:
                                        KIRIMKAN().PENGIKUT(session, self.USERNAME, self.PASSWORD, HOST, self.YOUR_USERNAME)
                                        continue
                                except SSLError:
                                    FAILED.append(f'{HOST}')
                                    BAD.append(f'{HOST}')
                                    CHECKPOINT.append(f'{HOST}')
                                    printf(f"[bold bright_black]   ──>[bold red] فشل الاتصال بخدمة {str(HOST).split('.')[0].upper()}!          ", end='\r')
                                    time.sleep(2.5)
                                    continue
                            if len(CHECKPOINT) >= 5:
                                printf(Panel(
                                    "[bold red]تم اكتشاف محاولة دخول غير آمنة لحسابك! يرجى الموافقة على تسجيل الدخول من جهازك الآخر،\n"
                                    "ثم أعد المحاولة.",
                                    width=59, style="bold bright_black",
                                    title="[bold bright_black]تحذير أمان"
                                ))
                                sys.exit()
                            elif len(BAD) >= 5:
                                printf(Panel(
                                    "[bold red]كلمة المرور غير صحيحة. ننصح بعدم استخدام حسابات جديدة لأنها قد لا تعمل مع هذه الخدمة!",
                                    width=59, style="bold bright_black",
                                    title="[bold bright_black]فشل تسجيل الدخول"
                                ))
                                sys.exit()
                            elif len(FAILED) >= 5:
                                printf(Panel(
                                    "[bold red]حدث خطأ غير معروف أثناء تسجيل الدخول. قد تكون الخدمة قيد الصيانة أو هناك مشكلة في الحساب!",
                                    width=59, style="bold bright_black",
                                    title="[bold bright_black]خطأ في الاتصال"
                                ))
                                sys.exit()
                            else:
                                if len(STATUS) != 0:
                                    try:
                                        self.DELAY(0, 300, self.YOUR_USERNAME)
                                        self.JUMLAH = INFORMASI().PENGIKUT(your_username=self.YOUR_USERNAME, updated=False)
                                    except Exception:
                                        self.JUMLAH = 'غير معروف'
                                    printf(Panel(
                                        f"""[bold white]الحالة :[bold green] تم إرسال المتابعين بنجاح!
[bold white]الرابط :[bold red] https://www.instagram.com/{str(self.YOUR_USERNAME)[:20]}
[bold white]العدد :[bold yellow] {self.JUMLAH}""",
                                        width=59, style="bold bright_black",
                                        title="[bold bright_black]نجاح العملية"
                                    ))
                                    self.DELAY(0, 600, self.YOUR_USERNAME)
                                    STATUS.clear()
                                    continue
                                else:
                                    self.DELAY(0, 600, self.YOUR_USERNAME)
                                    continue
                        except RequestException:
                            printf(f"[bold bright_black]   ──>[bold red] مشكلة في اتصالك بالإنترنت!          ", end='\r')
                            time.sleep(9.5)
                            continue
                        except KeyboardInterrupt:
                            printf(f"                               ", end='\r')
                            time.sleep(2.5)
                            continue
                        except Exception as e:
                            printf(f"[bold bright_black]   ──>[bold red] {str(e).upper()}!", end='\r')
                            time.sleep(5.5)
                            continue
                else:
                    printf(Panel(
                        "[bold red]لم تُدخل اسم مستخدم صالحًا. تأكد من كتابته بشكل صحيح وأن الحساب غير مقفول!",
                        width=59, style="bold bright_black",
                        title="[bold bright_black]اسم المستخدم غير صحيح"
                    ))
                    sys.exit()
            else:
                printf(Panel(
                    "[bold red]لم تُدخل بيانات الحساب بشكل صحيح. تأكد من استخدام الرمز ':' بين اسم المستخدم وكلمة المرور!",
                    width=59, style="bold bright_black",
                    title="[bold bright_black]خطأ في التنسيق"
                ))
                sys.exit()
        except Exception as e:
            printf(Panel(
                f"[bold red]{str(e).capitalize()}!",
                width=59, style="bold bright_black",
                title="[bold bright_black]خطأ غير متوقع"
            ))
            sys.exit()

    def LOGO(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        printf(Panel(r"""[bold red] _____                      ______            _
(_____)           _        |  ___ \          | |
   _   ____   ___| |_  ____| | _ | | ___   _ | | ____
  | | |  _ \ /___)  _)/ _  | || || |/ _ \ / || |/ _  |
 _| |_| | | |___ | |_( ( | | || || | |_| ( (_| ( ( | |
[bold white](_____)_| |_(___/ \___)_||_|_||_||_|\___/ \____|\_||_|_
        [underline green]زيادة متابعين إنستغرام مجانًا - بواسطة صلاح الدين بادي""", width=59, style="bold bright_black"))
        return True

    def DELAY(self, menit, detik, your_username):
        self.TOTAL = (menit * 60 + detik)
        while self.TOTAL:
            MENIT, DETIK = divmod(self.TOTAL, 60)
            printf(f"[bold bright_black]   ──>[bold green] @{str(your_username)[:20].upper()}[bold white]/[bold green]{MENIT:02d}:{DETIK:02d}[bold white] ناجح:-[bold green]{len(SUKSES)}[bold white] فشل:-[bold red]{len(GAGAL)}     ", end='\r')
            time.sleep(1)
            self.TOTAL -= 1
        return True

if __name__ == '__main__':
    try:
        if not os.path.exists("Penyimpanan/Subscribe.json"):
            youtube_url = json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/InstaModa/main/Penyimpanan/Youtube.json').text)['Link']
            os.system(f'start {youtube_url}' if os.name == 'nt' else f'xdg-open {youtube_url}')
            os.makedirs("Penyimpanan", exist_ok=True)
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                w.write(json.dumps({"Status": True}))
            time.sleep(2.5)
        if os.path.exists(".git"):
            os.system('git pull')
        MAIN()
    except Exception as e:
        printf(Panel(
            f"[bold red]{str(e).capitalize()}!",
            width=59, style="bold bright_black",
            title="[bold bright_black]خطأ"
        ))
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()
