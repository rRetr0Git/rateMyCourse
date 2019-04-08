# git分支管理

大家只需要进行feature分支部分的操作，即新建feature分支、commit多次，merge到develop即可，其他部分有专人处理。

## 常用指令

+ 推荐使用git bash进行git操作。

+ xxx代替具体名称，但是不要省略鸭。

+ 熟悉以后尽量不要复制过去鸭，慢慢就能不看文档打下来了。

```
从github克隆我们的项目到本地
在正确的本地路径下git clone git@github.com:rRetr0Git/rateMyCourse.git

查看本地分支
git branch

查看本地和远程分支
git branch -a

切换本地分支xxx
git checkout xxx

创建新本地分支xxx
git branch xxx

创建新本地分支xxx并切换过去
git checkout -b xxx

查看本地文件状态
git status

提交xxx文件
git add xxx
git commit -m "xxx"

推送到远程xxx分支
git push origin xxx

拉取远程xxx分支的更新
git pull origin xxx
```

```
add了多余文件xxx
git reset HEAD xxx

commit后发现有文件xxx忘了加入
git add xxx
git commit --amend

撤销本地commit到上一个commit，但保留对文件的修改
git reset --soft HEAD^
然后重新commit

撤销push到远程xxxx分支的commit（版本号为xx，版本号通过git log查），但保留对文件的修改，并重新commit，push
git reset --soft xx
git push origin xxxx --force 
然后重新add，commit，push

删除远程文件
git rm -r -n --cached xxx
git rm -r --cached xxx
git commit -m "xxx"
git push origin xx
```


## 一些约定

+ 任何一次add前，请用git branch查看所在分支是否正确，用git status查看修改的文件。

+ 任何一次commit前，请用git status查看add的文件有没有多余的。

+ 任何一次出现错误的add、commit、push行为，请通知群里不要改动分支，然后处理。

## 主分支

### master分支

+ master的每次commit都必须是一个正式的大版本更新，必须打tag。
+ 只能通过merge release分支来修改，其他时候不要修改master。

### develop分支

+ 用于开发工作，每个人都从develop上分出新分支开发，开发完成后合入develop分支。

## 其他分支

### feature分支

+ 用于每个人分配到的新功能相关代码。

+ 必须从develop分出来，必须合入develop，合入后删除该分支。

+ feature分支不能出现在origin，即只能commit不能push。

+ feature分支的命名基本无要求，如“wwj”

```
# 创建feature分支
任意分支下git checkout -b wwj develop

# 每次有代码更新，在feature分支提交，只commit不push
git add xxx
git commit -m "xxx"

# 完成该阶段工作，合并到develop分支，并删除wwj分支
git checkout develop
git pull origin develop
git merge --no-ff wwj
git branch -d wwj
git push origin develop
```

### release分支

+ 用于发布正式版本。当develop上所有功能都完成后，创建release分支，此后不允许添加新功能，但可以在release分支上debug。而后会合并如master（为了发布）和develop分支（为了将fixbug部分移入develop）。

+ 必须从develop分出来，必须合入develop和master。

+ release创建出来后到删除前，所有的bugfix请直接在release分支上修改。

+ 命名必须为“release-\*”，如“release-0.2”，数字为版本号。版本号具体怎么来一般以公司dalao心情决定，一般是A.B.C的格式，A是大版本号，B是增加新功能，C是修复bug。我们发布的次数有限，我推荐直接用A.B格式，把新功能和修复bug都在B递增，预计会在网站可以完全运行时更新大版本到1.0。即从0.1,0.2...0.10,0.11,0.12....1.0,1.1,1.2这样来。

```
# 创建release分支
任意分支下git checkout -b release-0.1 develop

# 在release分支下fix bug
git branch -a
git checkout release
git add xxx
git commit -m "xxx"
git push origin release

# 把release分支合并到master分支和develop分支
git checkout master
git merge --no-ff release-0.1
git tag 0.1
git checkout develop
git merge --no-ff release-0.1
git branch -d release-0.1
git push --tags
git push
```

