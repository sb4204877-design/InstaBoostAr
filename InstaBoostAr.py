try:
    from requests.exceptions import RequestException
    import requests, re, json, time, os, sys
    from rich.console import Console
    from rich.table import Table
    from rich import print as printf
    from requests.exceptions import SSLError
except (ModuleNotFoundError) as e:
    sys.exit(f"[خطأ] {str(e).capitalize()}!")

SUKSES, GAGAL, FOLLOWERS, STATUS, BAD, CHECKPOINT, FAILED, TRY = [], [], {"COUNT": 0}, [], [], [], [], []

class KIRIMKAN:
    def __init__(self): pass

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
            'Host': host,
            'Sec-Fetch-Dest': 'document',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Connection': 'keep-alive'
        })
        response = session.get(f'https://{host}/login')
        token_match = re.search(r'"&antiForgeryToken=(.*?)";', response.text)
        if not token_match:
            printf(f"[red]   ──> لم يتم العثور على رمز الأمان في {host}!")
            time.sleep(2.5)
            return False

        token = token_match.group(1)
        session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': f'https://{host}/login',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': '; '.join(f"{k}={v}" for k, v in session.cookies.get_dict().items()),
            'Origin': f'https://{host}'
        })
        data = {'username': username, 'antiForgeryToken': token, 'userid': '', 'password': password}
        response2 = session.post(f'https://{host}/login?', data=data)
        json_resp = response2.json()

        if "'status': 'success'" in str(json_resp):
            session.headers['Referer'] = f'https://{host}/tools/send-follower'
            session.headers['Cookie'] = '; '.join(f"{k}={v}" for k, v in session.cookies.get_dict().items())
            data = {'username': your_username}
            response3 = session.post(f'https://{host}/tools/send-follower?formType=findUserID', data=data)
            if 'name="userID"' in response3.text:
                user_id = re.search(r'name="userID" value="(\d+)">', response3.text).group(1)
                session.headers['Cookie'] = '; '.join(f"{k}={v}" for k, v in session.cookies.get_dict().items())
                data = {'userName': your_username, 'adet': '500', 'userID': user_id}
                response4 = session.post(f'https://{host}/tools/send-follower/{user_id}?formType=send', data=data)
                json_resp4 = response4.json()
                if "'status': 'success'" in str(json_resp4):
                    SUKSES.append(str(json_resp4))
                    STATUS.append(str(json_resp4))
                elif "'code': 'nocreditleft'" in str(json_resp4):
                    printf("[red]   ──> انتهت رصيدك في الخدمة!")
                    time.sleep(4.5)
                elif "'code': 'nouserleft'" in str(json_resp4):
                    printf("[red]   ──> لا يوجد مستخدمون متاحون!")
                    time.sleep(4.5)
                elif 'istek engellendi.' in str(json_resp4):
                    TRY.append(str(json_resp4))
                    if len(TRY) >= 3:
                        TRY.clear()
                        printf("[red]   ──> تم حظر طلب إرسال المتابعين!")
                        time.sleep(4.5)
                        return False
                    else:
                        return self.PENGIKUT(session, username, password, host, your_username)
                else:
                    GAGAL.append(str(json_resp4))
                    printf("[red]   ──> خطأ أثناء إرسال المتابعين!")
                    time.sleep(4.5)
                printf(f"[green]   ──> اكتمل الإرسال من خدمة {host.split('.')[0].upper()}!")
                time.sleep(5.0)
                return True
            else:
                printf("[red]   ──> اسم المستخدم غير موجود!")
                time.sleep(4.5)
                return False
        elif 'Güvenliksiz giriş tespit edildi.' in str(json_resp):
            CHECKPOINT.append(str(json_resp))
            printf("[red]   ──> حسابك يحتاج تحقق أمني!")
            time.sleep(4.5)
            return False
        elif 'Üzgünüz, şifren yanlıştı.' in str(json_resp):
            BAD.append(str(json_resp))
            printf("[red]   ──> كلمة المرور غير صحيحة!")
            time.sleep(4.5)
            return False
        else:
            FAILED.append(str(json_resp))
            printf("[red]   ──> خطأ في تسجيل الدخول!")
            time.sleep(4.5)
            return False

class INFORMASI:
    def __init__(self): pass

    def PENGIKUT(self, your_username, updated):
        global FOLLOWERS
        with requests.Session() as s:
            s.headers.update({
                'User-Agent': 'Instagram 317.0.0.0.3 Android',
                'Host': 'i.instagram.com',
                'Accept-Language': 'ar,en;q=0.9',
            })
            resp = s.get(f'https://i.instagram.com/api/v1/users/web_profile_info/?username={your_username}')
            if '"status":"ok"' in resp.text:
                count = json.loads(resp.text)['data']['user']['edge_followed_by']['count']
                if updated:
                    FOLLOWERS["COUNT"] = int(count)
                    return True
                else:
                    diff = int(count) - FOLLOWERS["COUNT"]
                    return f"+{diff} > {count}"
            else:
                if updated:
                    FOLLOWERS["COUNT"] = 0
                return "-+500"

class MAIN:
    def __init__(self):
        global CHECKPOINT, BAD, FAILED
        console = Console()
        os.system('cls' if os.name == 'nt' else 'clear')

        # --- جدول بسيط للترحيب ---
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_row("[bold white]أداة زيادة متابعين إنستغرام")
        table.add_row("[dim]الإصدار: 1.0 | بدون شعار | بدون اشتراكات")
        printf(table)
        print()

        # --- إدخال الحساب الوهمي ---
        print("[bold cyan]أدخل بيانات الحساب الوهمي (username:password):[/]", end=" ")
        accounts = input().strip()
        if ':' not in accounts:
            print("[red]خطأ: يجب استخدام ':' كفاصل بين الاسم وكلمة المرور!")
            sys.exit(1)

        username, password = accounts.split(':', 1)
        print("[bold cyan]أدخل اسم المستخدم المستهدف (بدون @):[/]", end=" ")
        target = input().strip().replace('@', '')
        if not target:
            print("[red]خطأ: يجب إدخال اسم مستخدم صالح!")
            sys.exit(1)

        print("\n[bold green]جارٍ بدء العملية... اضغط Ctrl+C للتوقف المؤقت.[/]\n")

        while True:
            try:
                INFORMASI().PENGIKUT(target, updated=True)
                CHECKPOINT.clear(); BAD.clear(); FAILED.clear()
                for host in ['instamoda.org', 'takipcitime.com', 'takipcikrali.com', 'bigtakip.net', 'takipcimx.net']:
                    try:
                        with requests.Session() as s:
                            KIRIMKAN().PENGIKUT(s, username, password, host, target)
                    except SSLError:
                        printf(f"[red]   ──> فشل الاتصال بـ {host.split('.')[0].upper()}!")
                        time.sleep(2.5)

                if len(CHECKPOINT) >= 5:
                    print("\n[red]الحساب موقوف مؤقتًا (Checkpoint). أعد المحاولة لاحقًا.")
                    break
                elif len(BAD) >= 5:
                    print("\n[red]كلمة المرور غير صحيحة. تأكد من الحساب الوهمي.")
                    break
                elif len(FAILED) >= 5:
                    print("\n[red]فشل متكرر في الاتصال. تحقق من الإنترنت أو الخدمة.")
                    break

                if STATUS:
                    try:
                        self.delay(300, target)
                        jumlah = INFORMASI().PENGIKUT(target, updated=False)
                    except:
                        jumlah = "غير معروف"
                    print(f"\n[green]✓ نجاح! العدد: {jumlah}\n")
                    STATUS.clear()
                    self.delay(600, target)
                else:
                    self.delay(600, target)

            except KeyboardInterrupt:
                print("\n[bold yellow]تم الإيقاف يدويًا.[/]")
                break
            except RequestException:
                print("[red]   ──> مشكلة في الاتصال بالإنترنت!")
                time.sleep(9.5)
            except Exception as e:
                print(f"[red]   ──> خطأ: {str(e)}!")
                time.sleep(5.5)

    def delay(self, seconds, username):
        for i in range(seconds, 0, -1):
            mins, secs = divmod(i, 60)
            print(f"\r[bold blue]انتظر: {mins:02d}:{secs:02d} | @{username[:15]} | ناجح: {len(SUKSES)} | فشل: {len(GAGAL)}", end="", flush=True)
            time.sleep(1)
        print()

if __name__ == '__main__':
    try:
        if os.path.exists(".git"):
            os.system('git pull')
        MAIN()
    except KeyboardInterrupt:
        print("\n[bold yellow]تم الخروج.[/]")
    except Exception as e:
        print(f"\n[red]خطأ غير متوقع: {e}[/]")
