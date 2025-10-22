```
要求
1.函数包装器有类型提示
2.state_name和class名重复写了
3.transfunc函数里面对tasks能修改，缓解部分的状态机爆炸
4.bufcnt没写

问题：
1.trans始终只能很短，lambda只能一句话。

todo:
1.函数包装器有类型提示：为什么要新建一个类？不直接把这个作为function包装进去？ √
2.state_name和class名重复写了 √
3.bufcnt没写 √
4.第二种状态机的方式使用状态模式 并把munkres写好（可能会用到wrapper？） √
5.继续绑定剩下的skill √
6.完成messi脚本 √
7.解决setNumberHard √
8.setNum不能给外界使用 √
9.裁判盒系统

如果新方式继续写下去，那么就会回到gsh模式

感觉包装是必要的，因为最后传入的第一位的参数是必须后面指定的。不多层包装根本写不下去

StateMachine()
State s;
s.name
s.tra
StateMachine.add_state(GO_FORWARD())

## 关于匹配：
路线1：完全放弃匹配，使用if调控好（现有的cpp层，但是还是要用到munkres可能）
路线2：match只能传定点，删去非NamedTasks层，roleMatch的中括号用优先级数字代替，处理好roleNumber问题
路线3：老的方法，用上一帧
```


**WARNING: Python 的函数默认参数 只在函数定义时计算一次，不是每次调用时重新计算。**



## 迁移的名称对应表

先用AI翻译，prompt:
```text
把enemy.lua的代码翻译为python，保留命名不变
```

剩下的进行文本替换即可
```
param. -> Params. (需import)
Utils. -> CppPackage.
player -> Player
    player.pos -> Player.Pos
vision. -> VisionModule().
bufcond -> buffered_condition
pos. -> Position. 注意一定要带点进行查找！不然会和ball的pos冲突替换！
ball.pos() -> Ball.pos() （Ball.py中的pos()函数）
    或者ball.Pos() （Vision中的实例ball的Pos()成员函数）
    注意！只有Ball.py中定义了posX之类的函数！所以都是需要把ball->Ball然后import！
gRoleNum[role] -> Global.getRoleNumber(role)

skillUtils没有全部绑定，有些用不上，可以暂时先注释掉
posmodule.getPos -> CppPackage.getPosModulePos
vision.getCircle()之类的，是导入Vision包下面的vision实例！！！

kick.lua直接替换到了WorldModel.__init__中的一个简单的枚举类型
kp. -> KickPower.
cp. -> ChipPower.
```
