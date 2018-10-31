# import scrapy
# from baekjoon.items import RankingItem
#
# # 나와 같은 페이지에 있는 사람들이 가장 많이 푼 문제순으로 알려주깅!
# class RankingSpider(scrapy.Spider):
#     name= "ranking"
#
#     # start_requests(self) 를 하면 여러개의 url을 파싱할 수 있는 것 같다.
#     def start_requests(self):
#         my_id = input("Insert your ID: ")
#         url = 'https://www.acmicpc.net/user/'+my_id+'/'
#         yield scrapy.Request(url=url,callback=self.myinfo_parse)
#
#     def myinfo_parse(self, response):
#         # get Solved Problems And my Ranking
#         ranks = response.xpath("//tr[1]/td/text()").extract_first()
#         page = int(int(ranks) / 100) + 1
#         my_id = response.url.split('/')[-2]
#         prob_list = []
#         for probs in response.xpath("//div[@class='panel-body']/span[/a").extract():
#
#     def comp_prob_parse(self, response):
#         prob_list = response.meta.get('prob_list')
#         is_solve = response.meta.get('is_solve')
#         comp_id = response.meta.get('comp_id')
#         next = response.xpath("//*[@id='next_page']/@href").extract_first()
#         for prob in response.xpath("//tbody/tr"):
#             num = int(prob.xpath("td[3]/a/text()").extract_first())
#             if (num in is_solve and is_solve[num] is True):
#                 item = RankingItem()
#                 item['prob_num'] = str(num)
#                 item['prob_title'] = prob.xpath("td[3]/a/@title").extract_first()
#                 item['prob_url'] = "https://www.acmicpc.net"+ prob.xpath("td[3]/a/@href").extract_first()
#                 item['prob_solve_date'] = prob.xpath("td[9]/a/@title").extract_first()
#                 prob_list.append(item)
#                 is_solve[num] = False
#
#         if (next is not None):
#             next_url = "https://www.acmicpc.net%s" % next
#             try:
#                 next_resp = yield scrapy.Request(url=next_url,callback=self.comp_prob_parse, meta={'prob_list': prob_list, 'is_solve': is_solve,'comp_id': comp_id})
#             except Exception:
#                 self.logger.info("Failed Request %s",next_url,exc_info = True)
#         else:
#             prob_list.reverse()
#             f = open(str(comp_id) + ".md",encoding='utf-8', mode='w')
#             f.write('# '+comp_id + " Solved "+str(len(prob_list))+"! \n")
#             for prob in prob_list:
#                 f.write('### '+prob['prob_num'] +" "+ prob['prob_title']+" "+ prob['prob_solve_date']+ '\n')
#                 f.write('### ['+prob['prob_num']+']('+prob['prob_url']+')\n')
#                 f.write('\n\n')
#             f.close()
#             print("Done! Study Hard :)")