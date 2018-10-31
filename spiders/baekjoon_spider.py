import scrapy
from baekjoon.items import BaekjoonItem


# 나와 비교하고 싶은 유저를 선택한 후, 내가 풀지 않은 문제 중 해당 유저가 푼 문제를 시간순으로!
class BaekjoonSpider(scrapy.Spider):
    name= "baekjoon"

    # start_requests(self) 를 하면 여러개의 url을 파싱할 수 있는 것 같다.
    def start_requests(self):
        my_id = input("Insert your ID: ")
        comp_id = input("Insert Competitor ID: ")
        url = 'https://www.acmicpc.net/vs/'+my_id+'/'+comp_id
        print(url)
        yield scrapy.Request(url=url,callback=self.prob_parse)

    def prob_parse(self, response):
        is_solve = {}
        prob_list =[]
        comp_id = response.url.split('/')[-1]
        for probs in response.xpath("//div[5]/div/div[2]/span[@class='problem_number']/a/text()").extract():
            is_solve[int(probs)] = True
            user_url = 'https://www.acmicpc.net/status?user_id='+comp_id+'&result_id=4'
            yield scrapy.Request(url=user_url, callback=self.comp_prob_parse, meta={'prob_list': prob_list,'is_solve': is_solve, 'comp_id': comp_id})
    def comp_prob_parse(self, response):
        prob_list = response.meta.get('prob_list')
        is_solve = response.meta.get('is_solve')
        comp_id = response.meta.get('comp_id')
        next = response.xpath("//*[@id='next_page']/@href").extract_first()
        for prob in response.xpath("//tbody/tr"):
            if (not prob.xpath("td[3]/a/text()")):
                continue
            num = int(prob.xpath("td[3]/a/text()").extract_first())
            if (num in is_solve and is_solve[num] is True):
                item = BaekjoonItem()
                item['prob_num'] = str(num)
                item['prob_title'] = prob.xpath("td[3]/a/@title").extract_first()
                item['prob_url'] = "https://www.acmicpc.net"+ prob.xpath("td[3]/a/@href").extract_first()
                item['prob_solve_date'] = prob.xpath("td[9]/a/@title").extract_first()
                prob_list.append(item)
                is_solve[num] = False

        if (next is not None):
            next_url = "https://www.acmicpc.net%s" % next
            print(next_url)
            try:
                next_resp = yield scrapy.Request(url=next_url,callback=self.comp_prob_parse, meta={'prob_list': prob_list, 'is_solve': is_solve,'comp_id': comp_id})
            except Exception:
                self.logger.info("Failed Request %s",next_url,exc_info = True)
        else:
            prob_list.reverse()
            f = open(str(comp_id) + ".md",encoding='utf-8', mode='w')
            f.write('# '+comp_id + " Solved "+str(len(prob_list))+"! \n")
            f.write('|문제 번호|문제 이름|푼 날짜|링크|해결|\n')
            f.write('|:---:|:---:|:---:|:---:|:---:|:----:|\n')
            for prob in prob_list:
                f.write('|'+prob['prob_num'] +'|'+ prob['prob_title']+'|'+ prob['prob_solve_date']+'|[링크]('+prob['prob_url']+')||\n')
            f.close()
            print("Done! Study Hard :)")
