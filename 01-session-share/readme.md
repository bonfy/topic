# Session共享

## 专题

创建一个网站之后，对于有些API可能需要优化，甚至是用其它语言优化，举个例子: python 实现的API响应速度慢，需要优化，又由于时间紧，不会重写所有API,只用 Go 重写部分的API, 这里面就要涉及到一个原有 Python 中的session 如何在Go中共享

## 基础知识 Session and Cookie

http是无状态的协议

1. session 在服务器端，cookie 在客户端（浏览器）
2. session 默认被存在在服务器的一个文件里（不是内存）
3. session 的运行依赖 session id，而 session id 是存在 cookie 中的，也就是说，如果浏览器禁用了 cookie ，同时 session 也会失效（但是可以通过其它方式实现，比如在 url 中传递 session_id）
4. session 可以放在 文件、数据库、或内存中都可以。
5. 用户验证这种场合一般会用 session 因此，维持一个会话的核心就是客户端的唯一标识，即 session id


## 实践

python 端口： 5000， go 端口: 8080

发现 python 中设置的 cookie 在 go中也能读取，所以可操作性就很强了

想法:

设置一个 username 或者 其它唯一标示的 cookie，然后将其它信息全部存于 数据库 或者 redis(利用唯一标识去读)， 就可以实现session 共享了

JWT 的话 两边的 SECRET_KEY 设置成一样就行了

## 参考

-[https://astaxie.gitbooks.io/build-web-application-with-golang/content/zh/06.1.html](https://astaxie.gitbooks.io/build-web-application-with-golang/content/zh/06.1.html)