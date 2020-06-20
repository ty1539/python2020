展示数据：

给模板一个字querySet 对象列表，循环出对象obj。

1. 普通字段

   obj.字段名    ——》 数据库中的数据

2. 外键

   obj.外键     ——》  外键的对象   给类定义`__str__`的方法

   obj.外键.字段

3. 带choices参数的

   obj.字段名    ——》 数据库中的数据  这个显示不是很好

   `obj.get_字段名_display()`     显示定义好的结果

4. 自定义方法

   ```python
   def show_publish_status(self):
       color_dict = {True: 'green', False: '#c35353'}
   
       return mark_safe(
           '<span style="background: {};color: white;padding: 3px" >{}</span>'.format(color_dict[self.publish_status],self.get_publish_status_display()))
   ```