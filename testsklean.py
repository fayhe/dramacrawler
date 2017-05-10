# coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.feature_extraction
import sklearn.naive_bayes as nb
import sklearn.externals.joblib as jl
import jieba
import os
from elasticsearch import Elasticsearch
import jieba.analyse
import jieba.posseg as pseg
from sklearn.svm import SVC 
from sklearn.feature_extraction.text import TfidfVectorizer

raw_data = []
category_list = []
es= Elasticsearch()

def fenci(summary):
	nlp_features_list = ""
	nlp_features = pseg.cut(summary)
	for w in nlp_features:
		##if w.flag == 'ns' or w.flag == 'n' or w.flag == 'ng' or w.flag == 'nl' or "a" in w.flag or "v" in w.flag or w.flag == 't':
			#print w.word + w.flag 
			nlp_features_list = nlp_features_list + " " + w.word 
	##jieba.analyse.extract_tags(summary,allowPOS=('ns', 'n','ng','nl','t','v','a'), topK=1000)
	#nlp_features_list = ' '.join(nlp_features)
	return nlp_features_list 


def generateRawDataList(type, category_label):


	#source = '/Users/fay/Downloads/dramacrawler/raw_data/' + movie_type
	#for root, dirs, filenames in os.walk(source):
	#	for f in filenames:
			##print f
	#		fullpath = os.path.join(source, f)
	#		log = open(fullpath, 'r')
			##print log.read()
	#		raw_data.append(log.read())
	#		category_list.append(category_label) 
	res = es.search(index="douban", doc_type=type, size=2000, body={"query": {"match_all": {}}})
	print("Got %d Hits:" % res['hits']['total'])
	for hit in res['hits']['hits']:
		id = hit["_id"]
		#print(hit["_id"])
		#title = hit["_source"]["alt_title"]
		#print(hit["_source"]["alt_title"])
		raw_data.append(fenci(hit["_source"]["summary"]))
		#print fenci(hit["_source"]["summary"])
		category_list.append(category_label)


def predict(summary, fh, svclf):
	kv = fenci(summary)
	#print kv
	mt = fh.transform([kv])
	##print mt
	num =  svclf.predict(mt)
	#num =  gnb.predict(mt)
	print num
	return num	

#fh =  TfidfVectorizer(sublinear_tf = True,  max_df = 0.5); 
generateRawDataList('剧情', 1)
generateRawDataList('喜剧', 2)
generateRawDataList('动作', 3) ## has bug
generateRawDataList('爱情', 4)
generateRawDataList('科幻', 5) ## has bug
#generateRawDataList('家庭', 5)
#generateRawDataList('纪录片', 5)
generateRawDataList('悬疑', 6)
#print raw_data

svclf = SVC(kernel = 'linear')#default with 'rbf' linear

fh =  TfidfVectorizer(sublinear_tf = True,  max_df = 0.5); 
#fh = sklearn.feature_extraction.FeatureHasher( non_negative=True,input_type='string')
#corpus = [
 #   '流感 / 战疫(港) 东南亚 艰险 来到 韩国 集装箱 全部 死亡 人 拖 身体 侥幸 逃入 闹市 携带 致命 猪 流感病毒 时间 病毒 迅速 蔓延 城市 角落 人 感染 死亡 阴影 引向 人 美丽 女医生 秀 爱 饰 是 单身 妈妈 不久前 遭遇 车祸 幸 消防队 救援 人员 饰 救出 丢失 重要 资料 备受 上司 苛责 值 韩国 蛇头 弟弟 流感 送入 仁海 医院 治疗 经 诊断 发现 流感 起因 死尸 横陈 集装箱 成为 查找 病源 关键 猪 流感病毒 成 爆发 蔓延 坐享 太平 民众 面临 灾难',
 #   '空中营救 / 急速天劫 饰 是 空警 奉命 飞往 伦敦 飞机 执行 任务 飞行 收到 未知 号码 发来 短信 人 举动 要求 秘密 账户 转账 会 每隔 杀死 航班 乘客 意识 到 事态 空姐 饰 乘客 饰 协助 试图 找出 人 事情 进展 超出 意料 本来 想 拯救 众人 意外 导致 人 死亡 乘客 当作 是否 能够 即 拯救 机上 乘客 洗脱 罪名'
 #]
#print corpus 
y = [0,1]
gnb = nb.MultinomialNB(alpha = 0.01)
#X = fh.fit_transform(corpus) TODO: trasform or fit tranform??
X = fh.fit_transform(raw_data)


svclf.fit(X,category_list)  
#gnb.fit(X, category_list)
#analyze = vectorizer.build_analyzer()

#print analyze("大型 傻逼 大 学生") 
print "爱在黎明"
summary = "美国青年杰西（伊桑·霍克 Ethan Hawke 饰）在火车上偶遇了法国女学生塞琳娜（朱莉·德尔佩 Julie Delpy 饰），两人在火车上交谈甚欢。当火车到达维也纳时，杰西盛情邀请塞琳娜一起在维也纳游览一番，即使杰西翌日便要坐飞机离开。与杰西一见钟情的塞琳娜接受了杰西的邀请。 他们一边游览城市，一边谈论着彼此的过去 ，彼此对生活的感想，两人了解越加深刻。他们非常珍惜这美妙的晚上，这对恋人一起经历了很多浪漫的经历因为他们约定在半年后再见，而此次约会将会在日出之间结束……"
predict(summary, fh, svclf)

print "喜欢你"
summary = "掌管跨国经济体的路晋（金城武 饰）刻薄挑剔，仅有美食这一个爱好。创意厨师顾胜男（周冬雨 饰）迷糊邋遢得过且过。一次收购，一道女巫汤，路晋喜欢上了顾胜男的菜却讨厌极了她这个人。喜欢还是讨厌究竟何去何从？"
predict(summary, fh, svclf)

print "xianyiren"
summary = "在刑警学院任职的物理天才唐川（王凯 饰）与中学教师石泓（张鲁一 饰）年少相识，因彼此对数学的共同兴趣而惺惺相惜，多年后唐川在调查一桩杀人案时， 身为石泓邻居的陈婧（林心如 饰）被列入警方的“嫌疑人”之中，石泓与唐川因此再度重逢，而唐川却在调查中发现了更大的秘密……被迫站在对立面的唐川、石泓由此展开了一场高智商对决，一步步推动故事走向既震撼人心又令人扼腕的结局。"
predict(summary, fh, svclf)	

print "怒"
summary = "炎炎夏日，东京八王子郊外社区，一对夫妇惨遭杀害。事后凶手用血在墙上写下大大的“怒”字，随后逃亡，销声匿迹长达一年之久。而在此期间，三个身份不明的男子和身边的人相遇了。曾自甘堕落的爱子（宫崎葵 饰）被父亲（渡边谦 饰）领回海滨小镇，邂逅了不善言辞的哲也（松山研一 饰）。在东京工作的同性恋优马（妻夫木聪 饰）将柔情似水的直人（绫野刚 饰）带回了家，他不相信对方，却又尝试去相信。随母亲搬到冲绳的小泉（广濑铃 饰）跟着同学辰哉（佐久本宝 饰）登上一座荒岛，在废墟中遇到了背包客田中（森山未来 饰），他们短暂成为朋友，而可怕的命运突然降临泉的头上。不久之后，通缉令遍布全国，三个男子的真实身份引人生疑……"
predict(summary, fh, svclf)	

print "三傻"
summary = "本片根据印度畅销书作家奇坦·巴哈特（Chetan Bhagat）的处女作小说《五点人》（Five Point Someone）改编而成。法兰（马德哈万 R Madhavan 饰）、拉杜（沙曼·乔希 Sharman Joshi 饰）与兰乔（阿米尔·汗 Aamir Khan 饰）是皇家工程学院的学生，三人共居一室，结为好友。在以严格著称的学院里，兰乔是个非常与众不同的学生，他不死记硬背，甚至还公然顶撞校长“病毒”（波曼·伊拉尼 Boman Irani 饰），质疑他的教学方法。他不仅鼓动法兰与拉杜去勇敢追寻理想，还劝说校长的二女儿碧雅（卡琳娜·卡普 Kareena Kapoor 饰）离开满眼铜臭的未婚夫。兰乔的特立独行引起了模范学生“消音器”（奥米·维嘉 Omi Vaidya 饰）的不满，他约定十年后再与兰乔一决高下，看哪种生活方式更能取得成功"
predict(summary, fh, svclf)	

print "食神"
summary = "史提芬周（周星驰 饰）在饮食界是享誉盛名的食神，但一直骄傲自大，惟利是图。被身边得力助手陷害，一夜间一无所有。他在庙街认识了早已对他倾心的大姐大火鸡（莫文蔚 饰）及一众老大，靠着史提芬周的商业头脑，他们决定推出“爆浆癞尿牛丸”，史提芬周重出江湖的道路也越来越顺利。为了重新夺得食神的位置，他回到大陆寻找“中国厨艺学院”受训。火鸡一路跟着他想对他表白，史提芬被对手追杀，火鸡不顾生命为他档了一枪，生死未卜。学成归来的史提芬如期到达食神的比赛场地，没想到评判却被对手收买了"
predict(summary, fh, svclf)	

print "我在姑姑秀文物"
summary = "重点记录故宫书画、青铜器、宫廷钟表、木器、陶瓷、漆器、百宝镶嵌、宫廷织绣等，该领域的稀世珍奇文物的修复过程和修复者的生活故事。片中第一次完整呈现世界顶级的中国文物修复过程和技术，展现文物的原始状态和收藏状态；第一次近距离展现文物修复专家的内心世界和日常生活；第一次完整梳理中国文物修复的历史源流；第一次通过对文物修复领域“庙堂”与“江湖”互动，展现传统中国四大阶层“士农工商”中唯一传承有序的“工”的阶层的传承密码，以及他们的信仰与变革"
predict(summary, fh, svclf)	

print "地球脉动"
summary = "BBC曾经制作出《蓝色星球》的纪录片摄影团队，再次集结奉上了这部堪称难以超越的经典纪录片《地球脉动》。从南极到北极，从赤道到寒带，从非洲草原到热带雨林，再从荒凉峰顶到深邃大海，难以数计的生物以极其绝美的身姿呈现在世人面前。我们看到了Okavango洪水的涨落及其周边赖以生存的动物们的生存状态，看到了罕见的雪豹在漫天大雪中猎食的珍贵画面；看到了冰原上企鹅、北极熊、海豹等生物相互依存的严苛情景，也见识了生活在大洋深处火山口高温环境下的惊奇生物。当然还有地球各地的壮观美景与奇特地貌，无私地将其最为光艳的一面展现出来。"
predict(summary, fh, svclf)	

print "记忆大师"
summary = "故事发生在2025年，因为和妻子张代晨（徐静蕾 饰）婚姻破裂，男主角江丰（黄渤 饰）走进记忆大师医疗中心接受手术，却不料手术失误记忆被错误重载，他莫名其妙变成了“杀人凶手”。警官沈汉强（段奕宏 饰）的穷追不舍让他逐渐发现，自己脑内的错误记忆不仅是破案的关键，更是救赎自己的唯一希望。与此同时，妻子身边出现的女人陈姗姗（杨子姗 饰）、记忆中浮现出的神秘女子（许玮甯 饰），似乎也和真相有着千丝万缕的联系，一场记忆烧脑战也随之开始。"
predict(summary, fh, svclf)	

print "独自在夜晚的海边"
summary = "某外国城市，来自韩国的女演员英熙，正因为和国内一个已婚男子的恋情而备受压力，她放弃了一切，甘受千夫所指以此表明心迹。他说会去找他，但她并不相信。在熟识的朋友家吃过饭，她去了海边。她认为朋友不会理解这段感情，但还是问道：“他会像我思念他一样思念我吗” 韩国江陵。几个老朋友的聚会。起初气氛有点尴尬，喝了些酒之后，英熙想吓吓他们。她表现得冷漠又不近人情，但他们反而喜欢这样。酒终人散，英熙独自去了海滩，发泄重重心事似雾般消散。她想知道，爱在生命中到底有多重要"
predict(summary, fh, svclf)

print "泰坦尼克号"
summary = "1912年4月10日，号称 “世界工业史上的奇迹”的豪华客轮泰坦尼克号开始了自己的处女航，从英国的南安普顿出发驶往美国纽约。富家少女罗丝（凯特•温丝莱特）与母亲及未婚夫卡尔坐上了头等舱；另一边，放荡不羁的少年画家杰克（莱昂纳多·迪卡普里奥）也在码头的一场赌博中赢得了下等舱的船票 罗丝厌倦了上流社会虚伪的生活，不愿嫁给卡尔，打算投海自尽，被杰克救起。很快，美丽活泼的罗丝与英俊开朗的杰克相爱，杰克带罗丝参加下等舱的舞会、为她画像，二人的感情逐渐升温。 1912年4月14日，星期天晚上，一个风平浪静的夜晚。泰坦尼克号撞上了冰山，“永不沉没的”泰坦尼克号面临沉船的命运，罗丝和杰克刚萌芽的爱情也将经历生死的考验。"
predict(summary, fh, svclf	)

print "情书"
summary = "日本神户某个飘雪的冬日，渡边博子（中山美穗）在前未婚夫藤井树的三周年祭日上又一次悲痛到不能自已。正因为无法抑制住对已逝恋人的思念，渡边博子在其中学同学录里发现“藤井树” 在小樽市读书时的地址时，依循着寄发了一封本以为是发往天国的情书。不想不久渡边博子竟然收到署名为“藤井树（中山美穗）”的回信，经过进一步了解，她知晓此藤井树是一个同她年纪相仿的女孩，且还是男友藤井树（柏原崇）少年时代的同班同学。为了多了解一些昔日恋人在中学时代的情况，渡边博子开始与女性藤井树书信往来。而藤井树在不断的回忆中，渐渐发现少年时代与她同名同姓的那个藤井树曾对自己藏了一腔柔情。"
predict(summary, fh, svclf	)

print "秒速5厘米"
summary = "如果，樱花掉落的速度是每秒5厘米，那么两颗心需要多久才能靠近？ 少年时，贵树（水橋研二配）和明理（近藤好美配）是形影不离的好朋友，可很快，一道巨大的鸿沟便横亘在两人中间：明理转学，贵树也随着父母工作的调动搬到遥远的鹿儿岛。在搬家前，贵树乘坐新干线千里迢迢和明理相会，在漫长的等待后，茫茫大雪中，两人在枯萎的樱花树下深情相拥，并献出彼此的first kiss，约定着下一次再一起来看樱花。 时光荏苒，两人竟再没见过，虽然在人海中一直搜寻彼此的身影，但似乎总是徒然。再后来，他们分别有了各自的生活，只是还偶尔会梦到13岁时的这段青涩而美好的感情，才明白当年怎么也说不出口的那个字就是爱。"
predict(summary, fh, svclf	)

print "我的少女时代"
summary = "成功白领林真心（陈乔恩 饰）因被上司压迫、下属吐槽，陷入了少女时代的深深回忆。原来曾是平凡少女（宋芸桦 饰）的真心有着一段爆笑却有充满甜蜜的初恋回忆。少女真心曾经暗恋校草欧阳非凡（李玉玺 饰），却总是不敌校花陶敏敏（简延芮 饰）的魅力，令她苦恼不已，一次意外却让她与校霸徐太宇（王大陆 饰）组成了“失恋阵线联盟”，他们势要夺爱，上演了一幕幕生猛、搞笑的青春趣事，而在相处中两人的情感也发生了微妙的变化……若干年后，来到成人世界的林真心又能否重拾初心呢？"
predict(summary, fh, svclf	)

print "完美陌生人"
summary = "七个常年的好朋友聚在一起吃晚餐。忽然他们决定与对方分享每一个短信的内容，包括他们收到的电子邮件和电话，由此许多秘密开始公布而他们之间的关系开始发生波动。"
predict(summary, fh, svclf	)

print "消失的爱人"
summary = "结婚五周年纪念日的早上，尼克·邓恩（本·阿弗莱克 Ben Affleck 饰）来到妹妹玛戈（凯莉·库恩 Carrie Coon 饰）的酒吧，咒骂抱怨那个曾经彼此恩爱缠绵的妻子艾米（罗莎蒙德·派克 Rosamund Pike 饰）以及全然看不见希望的婚姻。当他返回家中时， 却发现客厅留下了暴行的痕迹，而妻子竟不见了踪影。女探员朗达·邦妮（金·迪肯斯 Kim Dickens 饰）接到报案后赶来调查，而现场留下的种种蛛丝马迹似乎昭示着这并非是一件寻常的失踪案，其背后或许隐藏着裂变于夫妻之情的谋杀罪行。艾米的失踪通过媒体大肆渲染和妄加揣测很快闻名全国，品行不端的尼克被推上风口浪尖，至今不见踪影的爱人对他进行无情审判，你侬我侬的甜言蜜语早已化作以血洗血的复仇与折磨…… "
predict(summary, fh, svclf	)

print "杀人回忆"
summary = "1986年，韩国京畿道华城郡，热得发昏的夏天，在田野边发现一具女尸，早已发臭。小镇警察朴探员（宋康昊饰）和汉城来的苏探员（金相庆饰）接手案件，唯一可证实的是这具女尸生前被强奸过。线索的严重缺乏让毫无经验的朴探员和搭档曹探员（金罗河饰）只凭粗暴逼供和第六感推断，几次将犯罪 嫌疑人屈打成招。而苏探员客观冷静，据理分析，几次排除嫌疑，警察内部为了证明与推翻矛盾不断，然而无辜女子还是接二连三被残忍杀害，他们只好达成共识一起合作。此时，一个极其符合作案特征的小青年（朴海日饰）成为最大嫌疑人，警方神经绷紧地锁定住他，同时DNA检测报告也被送往美国，然而案件并未在此处停止。"
predict(summary, fh, svclf	)

print "男孩"
summary = "男孩在病房前看着沉睡的父亲做着自己的功课。数学不是很会写，但是闭着眼睛都会调点滴了，这是他每天生活的开始也是结束。直到有一天，一朵发亮的云将父亲带往天空中，男孩为了找回父亲，在变幻莫测的云中世界展开一场冒险的旅程。"
predict(summary, fh, svclf	)

print "《七种静默：忿怒》"
summary = "九月：从前有一个小孩，叫九月。九月出生的九月，他的妈妈说，这样很方便，不会忘记他的名字。九月没有姓，因为他有很多个爸爸，他妈妈每天都带不同的爸爸回家，这是妈妈的工作。九月和妈妈住在一栋小公寓里，他们一起睡一张床。床上挂了一张布帘子，布帘子一关上，妈妈就工作了，布帘子一拉开，妈妈就收工了；妈妈说，这样很方便。《忿怒》叙述妓女玛莉、失业工人未夏、垃圾婆刘玉宝、窃贼七只手与小男孩九月的故事。他们聚居在香港某栋破落的公屋里，或近或远地交织成一张无法挣脱的命运网络。未夏与玛莉是已分手的老相好，分手后玛莉和一位烂赌男子交往，欠下巨额高利贷。未夏失业多日，他的弟弟未冬专犯大案，未夏经常受到连累，吃足警察的苦头。七只手与好友阿雄仔，从大陆一块到香港闯荡，多年来一事无成，终究沦为窃贼。垃圾婆只身养育独子长大成人，晚年却被儿子抛弃，只得孤独地在垃圾堆中苟活。年纪小小的九月在不同大人间辗转流养，背负一切苦痛的记忆长大。炙热酷夏，香港社会底层五个人的生命，在一条被遗弃的怒狗吠声中交会……"
predict(summary, fh, svclf	)

print "攻壳机动队"
summary = "近未来，人类的各种器官均可实现移植，一时间机器人、生还人、仿生人充斥世间，与人类真假莫辨。某座繁华都市的大厦内，汉卡公司高管正与非洲来宾洽谈业务，突然宴会变成血腥大屠杀，暴走的机器人大开杀戒。隶属公安九课的米拉·基里安少佐（斯嘉丽·约翰逊 Scarlett Johansson 饰）带领巴特（皮鲁·埃斯贝克 Pilou Asbæk 饰）等手下赶往现场，平息事态。根据对暴走艺伎机器人的调查发现，被称作“久世”的神秘之人策划了这一系列的行动，而且他的目标全部指向了掌握着生化前沿尖端科技的汉卡公司及其研发人员。经过一番凶险的周旋，少佐逐渐逼近真相，同时也渐渐解开了发生在自己身上的惊天秘密"
predict(summary, fh, svclf	)

print "云图"
summary = "1850年，南太平洋，美国公证人亚当·尤因（吉姆·斯特吉斯 Jim Sturgess 饰）在船上被不明寄生虫病折磨，他用日记记录下自己所见所闻；1931年，苏格兰，落魄青年罗伯特·弗罗比舍（本·卫肖 Ben Whishaw 饰）为音乐大师记录曲谱，受到半本旅行日记的启发创作出了恢宏壮阔的《云图六重奏》；1975年，美国加州，小报记者路易莎·雷（哈莉·贝瑞 Halle Berry 饰）冒着生命危险调查一桩核电站丑闻，在老唱片店她被一首不知名的乐章打动；2012年，英国伦敦，被囚禁在养老院的出版商蒂莫西·卡文迪什（吉姆·布劳德本特 Jim Broadbent 饰）揣着一叠由女记者写成的纪实文学，打算将自己的“越狱经历”拍成电影；乌托邦未来，首尔，餐厅服务员克隆人星美-451（裴斗娜 Doona Bae 饰）开始形成自我意识和反抗人类，她在人类图书馆看了一部飞跃老人院的电影；文明毁灭后的未来，夏威夷，牧羊土着扎克里（汤姆·汉克斯 Tom Hanks 饰）对高科技文明的先知心怀敌意，他的部落唯一相信的女神叫星美…… 不同的人物、场景和事件在时空中更迭变幻，不变的是每个主角身上都带有彗星形状的胎记。它像亘古灵魂的烙印，将人性中的反抗精神代代延续，最终织成一幅浩瀚璀璨的云图"
predict(summary, fh, svclf	)

print "摔跤吧！爸爸摔跤吧！爸爸"
summary = "马哈维亚·辛格·珀尕（阿米尔·汗 Aamir Khan 饰）曾是印度国家摔跤冠军，因生活所迫放弃摔跤。他希望让儿子可以帮他完成梦想——赢得世界级金牌。结果生了四个女儿本以为梦想就此破碎的辛格却意外发现女儿身上的惊人天赋，看到冠军希望的他决定不能让女儿的天赋浪费，像其他女孩一样只能洗衣做饭过一生 ，再三考虑之后，与妻子约定一年时间按照摔跤手的标准训练两个女儿：换掉裙子 、剪掉了长发，让她们练习摔跤，并赢得一个又一个冠军，最终赢来了成为榜样激励千千万万女性的机会"
predict(summary, fh, svclf	)

print "银河护卫队2"
summary = "漫威影业最新力作《银河护卫队2》带着全新劲爆好听的“劲歌金曲第二辑”回归大银幕！银河护卫队在本集中穿越宇宙，继续外太空的史诗冒险之旅。他们必须共同作战，守护彼此；同时要解开“星爵”彼得·奎尔的身世之谜。旧日敌人变为盟友，漫画中深受喜爱的角色也会现身，对护卫队出手援助。漫威电影宇宙则将持续扩张，进入新纪元！"
predict(summary, fh, svclf	)

print "速度与激情8"
summary = "多米尼克（范·迪塞尔 Vin Diesel 饰）与莱蒂（米歇尔·罗德里格兹 Michelle Rodriguez 饰）共度蜜月，布莱恩与米娅退出了赛车界，这支曾环游世界的顶级飞车家族队伍的生活正渐趋平淡。然而，一位神秘女子Cipher（查理兹·塞隆 Charlize T heron 饰）的出现，令整个队伍卷入信任与背叛的危机，面临前所未有的考验。"
predict(summary, fh, svclf	)