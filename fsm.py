from transitions.extensions import GraphMachine

from utils import send_text_message, gossip_finder


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.nPush = 0
        self.keyword = ""
        self.count = 0

    def reset(self, event):
        text = event.message.text
        return text.lower() == "reset"

    def on_enter_user(self, event):
        print('welcome home')
        try:
            reply_token = event.reply_token
            send_text_message(reply_token, "輸入start開始搜尋批踢踢八卦版")
        except:
            print('no_event')

    def is_going_to_start(self, event):
        text = event.message.text
        return text.lower() == "start"

    def is_going_to_default_search(self, event):
        text = event.message.text
        return text.lower() == "d"

    def is_going_to_custom_search(self, event):
        text = event.message.text
        return text.lower() == "c"

    def get_keyword(self, event):
        return 1

    def is_goingback(self, event):
        text = event.message.text
        return text.lower() == "go back"

    def anykey(self, event):
        return 1

    def isValidnPush(self, event):
        number = event.message.text
        if number:  # 如果不是數字情況
            try:
                number = int(number)  # 數字
            except ValueError:
                return 0
        else:
            return 0
        return (-99 <= number <= 99)

    def isValidCount(self, event):
        number = event.message.text
        if number:  # 如果不是數字情況
            try:
                number = int(number)  # 數字
            except ValueError:
                return 0
        else:
            return 0
        return (1 <= number <= 15)

    def on_enter_start(self, event):
        print("I'm entering start")

        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎使用批踢踢八卦版爬蟲搜尋\n預設搜尋: 與關鍵字相符主題 5 筆\n客製化搜尋: 可設定關鍵字, 推文數量, 顯示幾筆資料(最多15筆)\n\n輸入 d - 使用預設搜尋(僅需輸入關鍵字)\n輸入 c - 客製化搜尋\n\n過程中可使用指令 \"reset\" 和 \"go back\" 來重置狀態")

    def on_exit_start(self, event):
        print("Leaving start")

    def on_enter_default_search_keyword(self, event):
        print("I'm entering default_search_keyword")

        reply_token = event.reply_token
        send_text_message(reply_token, "請直接輸入關鍵字")

    def on_exit_default_search_keyword(self, event):
        print("Leaving default_search_keyword")

    def on_enter_do_default_search(self, event):
        print("I'm entering do_default_search")

        reply_token = event.reply_token
        self.keyword = event.message.text
        text = "搜尋關鍵字: \"" + self.keyword + "\" 共 5 筆" + "\n\n" + gossip_finder(count=5, keyword=str(self.keyword), nPush=0) + '\n輸入任意鍵繼續'
        send_text_message(reply_token, text)

    def on_exit_do_default_search(self, event):
        print("Leaving do_default_search")

    def on_enter_done(self, event):
        print("search finished")
        self.go_back(event)

    def on_exit_do_default_search(self, event):
        print("go back to start")
    
    def on_enter_custom_search_keyword(self, event):
        print("I'm entering custom_search_keyword")

        reply_token = event.reply_token
        send_text_message(reply_token, "請直接輸入關鍵字")

    def on_exit_custom_search_keyword(self, event):
        print("Leaving custom_search_keyword")

    def on_enter_custom_search_nPush(self, event):
        print("I'm entering custom_search_nPush")

        self.keyword = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, "篩選推文數 -99 ~ +99\n(<0 則篩選噓文數, =0 無視推文數)")

    def on_exit_custom_search_nPush(self, event):
        print("Leaving custom_search_nPush")

    def on_enter_custom_search_count(self, event):
        print("I'm entering custom_search_count")

        self.nPush = int(event.message.text)
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入顯示文章數量 (1~15)")

    def on_exit_custom_search_count(self, event):
        print("Leaving custom_search_count")

    def on_enter_do_custom_search(self, event):
        print("I'm entering do_custom_search")

        self.count = int(event.message.text)
        reply_token = event.reply_token
        text = "搜尋關鍵字: \"" + str(self.keyword) + "\" 共 " + event.message.text + " 筆" + "\n\n" + gossip_finder(count=self.count, keyword=str(self.keyword), nPush=self.nPush) + '\n輸入任意鍵繼續'
        send_text_message(reply_token, text)

    def on_exit_do_custom_search(self, event):
        print("Leaving do_custom_search")        