from django.shortcuts import render


# Create your views here.
def template_test(request):
    num = 1
    string = 'alex is dsb'
    name_list = ['天然', '老毕', '老任']
    dic = {'name': 'alex', 'age': '73', 'keys': 'xxx'}
    tup = ('天然', '老毕', '老任')
    name_set = {'天然', '老毕', '老任'}

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def talk(self):
            return '你在无中生有 暗度存仓 凭空想象 凭空捏造'

        def __str__(self):
            return "< Person object {}:{} >".format(self.name, self.age)

    alex = Person('alex', 84)
    peiqi = Person('peiqi', 73)
    p_list = [alex, peiqi]

    import datetime
    now = datetime.datetime.now()

    return render(request,
                  'template_test.html',
                  {
                      'p_list': p_list,
                      'now': now,
                      'a': '<a href="http://www.luffycity.com">路飞</a>',
                      'num': num,
                      'string': string,
                      'name_list': name_list,
                      'dic': dic,
                      'tup': tup,
                      'name_set': name_set,
                      'alex': alex,
                      'baobei': '洪力君',
                      'kong': {},
                      'filesize': 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
                      'long_str': '你在无中生有 你在暗度陈仓 你在凭空想象 你在凭空捏造 你在无言无语 你在无可救药 你是逝者安息 你是一路走好 你是傻子巴拉 你是永无止境 你是没钱买药 你是头脑有病 你是眼里有泡 你是嘴里刘能 你是污言秽语 你是咎由自取 你是殃及无辜 你是祸害众生 你是仓皇失措 你是暗度陈仓 你是无可救药 你是无颜面对江东父老 你是人模狗样 你是臭气熏天'
                  })


def form(request):
    return render(request,'form.html')