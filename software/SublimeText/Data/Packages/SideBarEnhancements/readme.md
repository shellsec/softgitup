# Sidebar Enhancements

### In other languages

English - <https://github.com/SideBarEnhancements-org/SideBarEnhancements.git>

## 介绍

此版本为[Sidebar Enhancements](https://github.com/SideBarEnhancements-org/SideBarEnhancements)的中文版，为[Sublime Text](http://www.sublimetext.com/)侧栏文件和文件夹操作提供增强功能。

- 提供“删除”、“打开”和“剪贴板”操作。
- 关闭、移动、打开、恢复受重命名/移动命令的缓冲区。（甚至在文件夹上）
- 基本功能：新建文件/文件夹、编辑、打开/运行、打开文件位置、查找所选/父文件夹/项目、剪切、复制、粘贴、粘贴到父目录、重命名、移动、删除、刷新……
- 高级功能：可选复制URL编码后的路径、复制UTF-8编码的内容、复制base64转码后的内容（适合嵌入css）、复制快速生成img/a/script/style等标签内容
- 当删除操作受影响时，使用“首选项”来控制是否关闭缓冲区
- 允许在状态栏上显示“文件修改日期”和“文件大小”。（可能有点儿麻烦）

如下载后的压缩包打开后是这样的：
要摆脱ST的菜单项，请在“首选项” ->
“浏览资源包”里创建两个空文件

- `Default/Side Bar Mount Point.sublime-menu`
- `Default/Side Bar.sublime-menu`

## Installation

将此存储库的内容下载或克隆到 ST 的 Packages/文件夹中与包名称完全相同的文件夹中。

```
--SideBarEnhancements-5.0.23（一级文件夹）
----bin（二级文件夹）
----desktop（二级文件夹）
----edit（二级文件夹）
----Commands.sublime-commands(二级文件)
…
```
正确的形式是：
```
--bin（一级文件夹）
--desktop（一级文件夹）
--edit（一级文件夹）
--Commands.sublime-commands(一级文件)
…
```

- 首先请注意，该软件包只在 "文件夹 "部分而非 "打开文件 "部分添加了上下文菜单。
- 打开软件package文件夹。Main menu -\> Preferences -\> Browse Packages.
- 关闭 Sublime Text。
- 删除 "Packages/SideBarEnhancements "文件夹
- 删除 "User/SideBarEnhancements "文件夹
- 向上浏览一个文件夹，进入 "Installed Packages/"，检查是否有 SideBarEnhancements 实例并将其删除。
- 打开 ST，使用 "Package Control "转到 ： 删除软件包，检查 SideBarEnhancements 的任何实例并将其删除。
- 重新启动 ST
- 打开 ST，检查 "Package Control "中是否有任何关于 SideBarEnhancements 的条目（在 "Remove Package"部分和 "Enable Package "部分）。
- 重复上述步骤，直到发现没有关于 SideBarEnhancements 的条目。
- 重新启动 ST
- 安装。
- 安装成功


（请注意，从版本2.122104开始，此软件包不再提供快捷键设置，您需要手动将其添加到您的sublime-keymap文件中（请参阅下一节））
使用F12可以在浏览器中打开当前文件

`url_testing` 允许您设置本地服务器的URL，通过F12打开

`url_production`允许您设置产品服务器的URL，通过ALT + F12打开

- 右键单击侧栏上的任何文件，然后选择：“项目 - >编辑预览地址”
- 编辑此文件，并使用以下结构添加路径和URL：
<!-- -->

    {
        "S:/www/domain.tld":{
            "url_testing":"http://testing",
            "url_production":"http://domain.tld"
        },
        "C:/Users/luna/some/domain2.tld":{
            "url_testing":"http://testing1",
            "url_production":"http://productiontld2"
        }
    }

### 关于相对路径

假如我们有一个具有以下结构的项目

    Project/ < - root project folder
    Project/libs/
    Project/public/ < - the folder we want to load as "http://localhost/"
    Project/private/
    Project/experimental/ < - other folder we may run as experimental/test in another url "http://experimental/"

接着创建配置文件：

`Project/.sublime/SideBarEnhancements.json`

内容：

    {
        "public/":{
            "url_testing":"http://localhost/",
            "url_production":"http://domain.tld/"
        },
        "experimental/":{
            "url_testing":"http://experimental/",
            "url_production":"http://domain.tld/"
        },
        "":{
            "url_testing":"http://the_url_for_the_project_root/",
            "url_production":"http://the_url_for_the_project_root/"
        }
    }

...

您可以在任何地方创建配置文件“some/folder/.sublime/SideBarEnhancements.json”。

#### F12 快捷键冲突

在 Sublime Text 3 上，`F12` 键默认绑定到 `"goto_definition"` 命令。该包与该密钥冲突，这种情况不再发生。您现在需要手动添加按键：转到“Preferences -> Package Settings -> Side Bar -> Key Bindings - User”并添加以下任意内容：

    	[
    		{ "keys": ["f12"],
    			"command": "side_bar_open_in_browser" ,
    			"args":{"paths":[], "type":"testing", "browser":""}
    		},
    		{ "keys": ["alt+f12"],
    			"command": "side_bar_open_in_browser",
    			"args":{"paths":[], "type":"production", "browser":""}
    		},
    		{
    			"keys": ["ctrl+t"],
    			"command": "side_bar_new_file2"
    		},
    		{
    			"keys": ["f2"],
    			"command": "side_bar_rename"
    		},
    	]

## 在路径中查找的按键绑定：

您可能希望添加一个用于打开“在路径中查找..”的键

    [
    	{
    		"keys": ["f10"],
    		"id": "side-bar-find-files",
    		"command": "side_bar_find_files_path_containing",
    		"args": {
    			"paths": []
    		}
    	}
    ]


定位文件： `User/SideBarEnhancements/Open With/Side Bar.sublime-menu` （注意额外的子文件夹级别）。要打开它，请右键单击打开的项目中的任何文件，然后选择`Open With > Edit Applications...`

-在 OSX 上，“application”属性仅采用应用程序的_name_，手头的文件的完整路径将被传递到该应用程序，就像使用“open ...”一样，例如：“application”：“Google Chrome”
-在 OSX 上，不支持调用 _shell_ 命令。
-您应该将菜单项的标题和 ID 更改为唯一。

<!-- -->

    //application 1
    {
    	"caption": "Photoshop",
    	"id": "side-bar-files-open-with-photoshop",
    	"command": "side_bar_files_open_with",
    	"args": {
    		"paths": [],
    		"application": "Adobe Photoshop CS5.app", // OSX
    		"extensions":"psd|png|jpg|jpeg",  //any file with these extensions
    		"args":[]
    	}
    },

### 参数变量说明

- \$PATH - The full path to the current file, "C:\Files\Chapter1.txt"
- \$PROJECT - The root directory of the current project.
- \$DIRNAME - The directory of the current file, "C:\Files"
- \$NAME - The name portion of the current file, "Chapter1.txt"
- \$NAME_NO_EXTENSION - The name portion of the current file without the extension, "Chapter1"
- \$EXTENSION - The extension portion of the current file, "txt"

## 库使用说明

(check each license in project pages)

- "getImageInfo" to get width and height for images from "bfg-pages". See:
  <http://code.google.com/p/bfg-pages/>
- "desktop" to be able to open files with system handlers. See:
  <http://pypi.python.org/pypi/desktop>
- "send2trash" to be able to send to the trash instead of deleting for ever!.
  See: <http://pypi.python.org/pypi/Send2Trash>
- "hurry.filesize" to be able to format file sizes. See:
  <http://pypi.python.org/pypi/hurry.filesize/>
- "Edit.py" ST2/3 Edit Abstraction. See:
  <http://www.sublimetext.com/forum/viewtopic.php?f=6&t=12551>

## 源代码

<https://github.com/SideBarEnhancements/SideBarEnhancements>

## 论坛

<http://www.sublimetext.com/forum/viewtopic.php?f=5&t=3331>

# Contributors:

Thank you so much!

Aleksandar Urosevic, bofm, Dalibor Simacek, Devin Rhode, Eric Eldredge, Hewei Liu, Jeremy Gailor, Joao Antunes, Leif Ringstad, MauriceZ, Nick Zaccardi, Patrik Göthe, Peder Langdal, Randy Lai, Raphael DDL Oliveira, robwala, Stephen Horne, Sven Axelsson, Till Theis, Todd Wolfson, Tyler Thrailkill, Yaroslav Admin

## License

"None are so hopelessly enslaved as those who falsely believe they are free."
Johann Wolfgang von Goethe

Copyright (C) 2014-2022 Tito Bouzout

This license apply to all the files inside this program unless noted different
for some files or portions of code inside these files.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation. <http://www.gnu.org/licenses/gpl.html>

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/gpl.html>

## Helpful!? Donate to support this project

https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DD4SL2AHYJGBW
