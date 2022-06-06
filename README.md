# mbtileserver

一个基于 [mbtiles](https://github.com/mapbox/mbtiles-spec)
数据库格式的地图切片服务器。

![Build Status](https://github.com/consbio/mbtileserver/actions/workflows/test.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/consbio/mbtileserver/badge.svg?branch=master)](https://coveralls.io/github/consbio/mbtileserver?branch=master)
[![GoDoc](https://godoc.org/github.com/consbio/mbtileserver?status.svg)](http://godoc.org/github.com/consbio/mbtileserver)
[![Go Report Card](https://goreportcard.com/badge/github.com/consbio/mbtileserver)](https://goreportcard.com/report/github.com/consbio/mbtileserver)

目前支持 `png`, `jpg`, `webp`, 和 `pbf` (矢量切片)
切片数据库遵循 mbtiles 1.0 规格。 切片调用采用 XYZ 坐标结构, 基于墨克托坐标（ Web Mercator ）系统。
UTF8 格栅格式不再支持。

每个地图数据库增加了：

-   TileJSON 2.1.0 接口, 包含 mbtiles 数据库全部元数据.
-   每个地图数据库提供预览。
-   一个精简版 ArcGIS 切片服务器接口。

所有切片格式均在
[AWS t2.nano](https://aws.amazon.com/about-aws/whats-new/2015/12/introducing-t2-nano-the-smallest-lowest-cost-amazon-ec2-instance/)
虚拟机上成功运行，没有任何问题。

## 目标

-   为 Web 地图应用提供一个支持 mbtiles 格式的切片服务器。
-   尽可能的提高服务器速度。
-   能在资源有限的云服务器上运行 (有限的内存和CPU资源)。
-   容易部署和维护。

## Go版本要求

_要求 Go 1.16+._

`mbtileserver` 要跨平台部署，建议采用 Go 1.18+.

## 安装和部署

部署预编译的二进制格式

Linux 系统
复制mbtileserver可执行文件和tilesets文件夹（内含mbtiles数据库文件）到 `/usr/mbtileserver` 目录。
执行命令
```sh
$  /usr/mbtileserver/mbtileserver
```
Windows 系统
复制mbtileserver.exe, start.js文件和tilesets文件夹（内含mbtiles数据库文件）到系统。双击start.js开始运行（启动成功不会弹出任何窗口）。

下载项目 

```sh
$  go get git.euclideon.cn:3000/Euclideon/mapdl
```

此命令会下载和安装可执行文件 `mbtileserver`.

## 启动

添加项目到可执行路径 ($GOPATH/bin 到你的系统 $PATH)，运行命令:

```
$  mbtileserver --help
Serve tiles from mbtiles files.

Usage:
  mbtileserver [flags]

Flags:
  -c, --cert string            X.509 TLS certificate filename.  If present, will be used to enable SSL on the server. 增加SSL支持。
  -d, --dir string             Directory containing mbtiles files. Directory containing mbtiles files.  Can be a comma-delimited list of directories. (default "./tilesets") 指定mbtiles数据库存放目录。"./tilesets"是默认目录。
      --disable-preview        Disable map preview for each tileset (enabled by default) 关闭地图预览。默认开启。
      --disable-svc-list       Disable services list endpoint (enabled by default) 关闭地图列举接口。默认开启。
      --disable-tilejson       Disable TileJSON endpoint for each tileset (enabled by default) 关闭TileJSON接口。默认开启。
      --domain string          Domain name of this server.  NOTE: only used for AutoTLS. 指定服务器域名（仅用于AutoTLS服务器）。
      --dsn string             Sentry DSN 
      --enable-arcgis          Enable ArcGIS Mapserver endpoints 开启ArcGIS地图服务器接口。
      --enable-fs-watch        Enable reloading of tilesets by watching filesystem 开启文件系统监控，重新加载数据库。
      --enable-reload-signal   Enable graceful reload using HUP signal to the server process 开启手动重加载功能。
      --generate-ids           Automatically generate tileset IDs instead of using relative path 自动生成切片ID。
  -h, --help                   help for mbtileserver
  -k, --key string             TLS private key 指定TLS密钥。
  -p, --port int               Server port. Default is 443 if --cert or --tls options are used, otherwise 8000. (default -1) 指定服务器端口。默认端口8000, tls服务默认端口443。
  -r, --redirect               Redirect HTTP to HTTPS 重定向
      --root-url string        Root URL of services endpoint (default "/services") 服务根路径，默认"/services"。
  -s, --secret-key string      Shared secret key used for HMAC request authentication 
      --tiles-only             Only enable tile endpoints (shortcut for --disable-svc-list --disable-tilejson --disable-preview) 仅启动地图切片服务。等效于"--disable-svc-list --disable-tilejson --disable-preview" 命令。
  -t, --tls                    Auto TLS via Let's Encrypt 启用TLS加密。
  -v, --verbose                Verbose logging 显示详细日志。
```

运行一个地图切片服务器非常简单：只需要把地图切片服务器复制到"tilesets"目录即可。并且可以同时开启多个地图切片数据库。

程序会把数据库自动转换成适当的调用地址URL。例如数据库文件`<tile_dir>/foo/bar/baz.mbtiles` 会被转换成 `/services/foo/bar/baz`.

如果使用了 `--generate-ids` 启动选项, 会使用哈希算法自动生成每个数据库的ID，默认ID基于 `--dir`选项提供的相对地址。

当数据库发生变化（被删除，修改，或添加新数据库）的时候只需要重新启动服务或重加载服务即可。

如果启动时提供了DSN, 服务器的警告，错误，严重错误，异常都会发送到该主机。

如果使用了 `redirect` 选项, 服务器会同时监听80端口，并把它重定向到443端口。

如果使用了 `--tls` 选项, Let's Encrypt 服务会被自动使用. [这里](https://letsencrypt.org/repository/)了解更多他们的服务. 证书会被缓存到 `.certs` 目录. 请确保 `mbtileserver` 有该文件夹的写权限，否则程序会报错. 如果在`localhost` 地址启动服务，则不会自动生成密钥。

如果使用了 `--cert` 或 `--tls` 选项, 默认端口是 443.

也可以使用环境变量代替命令行选项, 这个特性在部署到 docker 镜像时非常有用。 例如环境变量:

-   `PORT` (`--port`)
-   `TILE_DIR` (`--dir`)
-   `GENERATE_IDS` (`--generate-ids`)
-   `ROOT_URL` (`--root-url`)
-   `DOMAIN` (`--domain`)
-   `TLS_CERT` (`--cert`)
-   `TLS_PRIVATE_KEY` (`--key`)
-   `HMAC_SECRET_KEY` (`--secret-key`)
-   `AUTO_TLS` (`--tls`)
-   `REDIRECT` (`--redirect`)
-   `DSN` (`--dsn`)
-   `VERBOSE` (`--verbose`)

示例:

```
$  PORT=7777 TILE_DIR=./path/to/your/tiles VERBOSE=true mbtileserver
```

docker-compose.yml 文件内容:

```
mbtileserver:
  ...

  environment:
    PORT: 7777
    TILE_DIR: "./path/to/your/tiles"
    VERBOSE: true
  entrypoint: mbtileserver

  ...
```

### 重加载

#### 命令行重加载

mbtileserver 支持热重载. 它需要在启动服务时使用 `--enable-reload-signal` 选项. 然后向服务器进程发送一个 `HUP` 信号:

```
$  kill -HUP <pid>
```

重加载将帮助服务器识别切片数据库的更改。

#### 使用文件系统监视重加载

mbtileserver  `--enable-fs-watch` 选项会启动服务监控指定目录的数据库文件，当这些文件发生修改时自动重加载数据库。

所有`-d` 或者 `--dir` 选项指定的目录，子目录内容都会被监控。

切片数据更新的时候会锁定数据库文件至少30秒. 这会导致期间发起的访问延时或返回 HTTP 503 错误，直到更新结束解除锁定。

警告: 服务器添加了自动更新切片功能后，不要开启文件系统监控选项。

### 使用反向代理

在 `mbtileserver` 和前端之间可以使用反向代理，例如要增加 TLS 加密等。

常用反向代理应用如 [`Caddy`](https://caddyserver.com/) 和 [`NGINX`](https://www.nginx.com/) 都被支持。

为保证启用TileJSON时URL正确 请确保反向代理添加了以下 headers:

协议 (HTTP 或者 HTTPS):
至少添加 `X-Forwarded-Proto`, `X-Forwarded-Protocol`, `X-Url-Scheme` 之一到服务请求中.
或者添加
`X-Forwarded-Ssl` 自动配置 HTTPS.

Host:
添加 `X-Forwarded-Host`.

#### Caddy v2 示例:

如果`mbtileserver` 运行在本地 8000 端口, 添加以下配置禁止域名:

```
<domain_name> {
  route /services* {
    reverse_proxy localhost:8000
  }
}
```

根据实际控制特定 `route` 中的缓存切片访问。例如, 防止客户端访问超过1小时的缓存切片:

```
  route /services* {
    header Cache-Control "public, max-age=3600, must-revalidate"
    localhost mbtileserver:8000
  }
```

#### NGINX 示例:

`mbtileserver` 运行在本地 8000 端口, 添加 `server` 配置:

```
server {
   <other config options>

    location /services {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://localhost:8000;
    }
}
```

## Docker

生成名为`mbtileserver`的 Docker 镜像 :

```
$  docker build -t mbtileserver -f Dockerfile .
```

在8080端口运行切片数据库在`<host tile dir>`的Docker 容器。
注意： `mbtileserver` 在容器中的默认端口是 8000。

```
$  docker run --rm -p 8080:8000 -v <host tile dir>:/tilesets  consbio/mbtileserver
```

增加别的启动选项, 例如启用`<host cert dir>`中的签名证书。

```
$  docker run  --rm -p 80:80 443:443 -v <host tile dir>:/tilesets -v <host cert dir>:/certs/ consbio/mbtileserver -c /certs/localhost.pem -k /certs/localhost-key.pem -p 443 --redirect
```

另外，还可以使用 `docker-compose` 运行:

```
$  docker-compose up -d
```

默认的 `docker-compose.yml` 配置文件使 `mbtileserver` 监听主机的 8080 端口, 使用 `./mbtiles/testdata` 目录中的数据库. 可以通过修改 `docker-compose.override.yml` 或 [扩展环境变量文件](https://docs.docker.com/compose/extends/) 来更改这些运行选项.

重加载服务:

```
$  docker exec -it mbtileserver sh -c "kill -HUP 1"
```

## 切片数据库规格

-   支持的 mbtiles version 1.0 文件规格说明 [mbtiles specification](https://github.com/mapbox/mbtiles-spec). 推荐 Version 1.1.
-   实现 [TileJSON 2.1.0](https://github.com/mapbox/tilejson-spec)

## 生成地图切片

可以使用多种工具生成地图切片数据库，如:

-   [TileMill](https://www.mapbox.com/tilemill/) (栅格图像切片)
-   [tippecanoe](https://github.com/mapbox/tippecanoe) (矢量切片)
-   [pymbtiles](https://github.com/consbio/pymbtiles) (Python生成切片)
-   [tpkutils](https://github.com/consbio/tpkutils) (ArcGIS生成栅格切片)

目录名会成为每个 mbtiles 数据库的 "tileset_id" 。

## XYZ 切片 API

形如:`/services/<tileset_id>/tiles/{z}/{x}/{y}.<format>`

`<format>` 可以是 `png`, `jpg`, `webp`, `pbf` 取决于数据库中切片的格式.

## TileJSON API

`mbtileserver` 会在`/services/<tileset_id>` 自动生成一个 TileJSON 接口。TileJSON 与切片使用相同的协议; `--domain` 选项不会影响生成的URL。该 API 输出 `metadata` 表中的大部分元数据.

例如：
`http://localhost/services/states_outline`

返回如下结果:

```
{
  "bounds": [
    -179.23108,
    -14.601813,
    179.85968,
    71.441055
  ],
  "center": [
    0.314297,
    28.419622,
    1
  ],
  "credits": "US Census Bureau",
  "description": "States",
  "format": "png",
  "id": "states_outline",
  "legend": "[{\"elements\": [{\"label\": \"\", \"imageData\": \"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IB2cksfwAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAGFJREFUOI3tlDEOgEAIBClI5kF+w0fxwXvQdjZywcZEtDI31YaQgWrdPsYzAPFGJCmmEAhJGzCash0wSVE/HHnlKcDMfrPXYgmXcAl/JswK6lCrz89BdGVm1+qrH0bbWDgA3WwmgzD8ueEAAAAASUVORK5CYII=\"}], \"name\": \"tl_2015_us_state\"}]",
  "map": "http://localhost/services/states_outline/map",
  "maxzoom": 4,
  "minzoom": 0,
  "name": "states_outline",
  "scheme": "xyz",
  "tags": "states",
  "tilejson": "2.1.0",
  "tiles": [
    "http://localhost/services/states_outline/tiles/{z}/{x}/{y}.png"
  ],
  "type": "overlay",
  "version": "1.0.0"
}
```

## Map 预览

`mbtileserver` 会在 `/services/<tileset_id>/map` 自动生成地图预览页面.

目前使用`Leaflet` 预览格栅图像地图； `Mapbox GL JS` 预览矢量地图。

## ArcGIS API

本项目提供一个精简版mbtiles格式的 ArcGIS 切片 API.

通过 `--enable-arcgis` 选项启动.

该服务需要mbtiles数据库满足特定的要求，如 [Data Basin](https://databasin.org). 因为 ArcGIS API 使用的一些属性在标准 mbtiles 数据库中并不常见。

该 API 并非为全功能的 ArcGIS 应用所设计，如 ArcGIS 桌面应用.

接口包括:

-   服务信息: `http://localhost:8000/arcgis/rest/services/<tileset_id>/MapServer`
-   图层信息: `http://localhost:8000/arcgis/rest/services/<tileset_id>/MapServer/layers`
-   切片: `http://localhost:8000/arcgis/rest/services/<tileset_id>/MapServer/tile/0/0/0`

## 调用认证

通过`-s/--secret-key` 选项提供密钥或设置`HMAC_SECRET_KEY` 环境变量会认证接口的调用。

### 生成签名证书

```go
serviceId := "test"
date := "2019-03-08T19:31:12.213831+00:00"
salt := "0EvkK316T-sBLA"
secretKey := "YMIVXikJWAiiR3q-JMz1v2Mfmx3gTXJVNqme5kyaqrY"

key := sha1.New()
key.Write([]byte(salt + secretKey))
```

生成哈希签名:

```go
hash := hmac.New(sha1.New, key.Sum(nil))
message := fmt.Sprintf("%s:%s", date, serviceId)
hash.Write([]byte(message))
```

最后，使用 base64-encode 编码哈希:

```go
b64hash := base64.RawURLEncoding.EncodeToString(hash.Sum(nil))
fmt.Println(b64hash) // Should output: 2y8vHb9xK6RSxN8EXMeAEUiYtZk
```

### 访问接口

认证访问必须包含 ISO 数据,和 salt-signature:`<salt>:<signature>`，如:

```text
?date=2019-03-08T19:31:12.213831%2B00:00&signature=0EvkK316T-sBLA:YMIVXikJWAiiR3q-JMz1v2Mfmx3gTXJVNqme5kyaqrY
```

或者在 request headers 中提供:

```text
X-Signature-Date: 2019-03-08T19:31:12.213831+00:00
X-Signature: 0EvkK316T-sBLA:YMIVXikJWAiiR3q-JMz1v2Mfmx3gTXJVNqme5kyaqrY
```

## 开发

Windows 系统需要安装 `gcc` 以编译 `mattn/go-sqlite3`源码.
MinGW or [TDM-GCC](https://sourceforge.net/projects/tdm-gcc/) 都可以供选择。

如果每次编译过程非常缓慢，可以先运行：

```
$  go build -a .
```

在`handlers/templates/static` 目录运行

```bash
$  npm install
```

安装`package.json` 文件中指定的前端依赖.

然后生成一个紧凑版本的前端:

```bash
$  npm run build
```
结果生成在 `handlers/templates/static/dist` 目录中
通过 `go:embed` 加入可执行文件.

修改任何 `.go` 文件，或 `handlers/templates` 目录中的文件，都需要重新运行 `go build .`.

## 版本变更

See [CHANGELOG](CHANGELOG.md).

## 代码贡献者 ✨

感谢这些优秀的开发者 ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://astutespruce.com"><img src="https://avatars2.githubusercontent.com/u/3375604?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Brendan Ward</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=brendan-ward" title="Code">💻</a> <a href="https://github.com/consbio/mbtileserver/commits?author=brendan-ward" title="Documentation">📖</a> <a href="https://github.com/consbio/mbtileserver/issues?q=author%3Abrendan-ward" title="Bug reports">🐛</a> <a href="#blog-brendan-ward" title="Blogposts">📝</a> <a href="https://github.com/consbio/mbtileserver/pulls?q=is%3Apr+reviewed-by%3Abrendan-ward" title="Reviewed Pull Requests">👀</a> <a href="#ideas-brendan-ward" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/fawick"><img src="https://avatars3.githubusercontent.com/u/1886500?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Fabian Wickborn</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=fawick" title="Code">💻</a> <a href="https://github.com/consbio/mbtileserver/commits?author=fawick" title="Documentation">📖</a> <a href="https://github.com/consbio/mbtileserver/issues?q=author%3Afawick" title="Bug reports">🐛</a> <a href="#ideas-fawick" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/nikmolnar"><img src="https://avatars1.githubusercontent.com/u/2422416?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nik Molnar</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=nikmolnar" title="Code">💻</a> <a href="#ideas-nikmolnar" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/consbio/mbtileserver/issues?q=author%3Anikmolnar" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://sikmir.ru"><img src="https://avatars3.githubusercontent.com/u/688044?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nikolay Korotkiy</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=sikmir" title="Code">💻</a> <a href="https://github.com/consbio/mbtileserver/issues?q=author%3Asikmir" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/retbrown"><img src="https://avatars1.githubusercontent.com/u/3111954?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Robert Brown</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=retbrown" title="Code">💻</a></td>
    <td align="center"><a href="mika-go-13"><img src="https://avatars.githubusercontent.com/u/26978815?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mihail</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=mika-go-13" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/buma"><img src="https://avatars2.githubusercontent.com/u/1055967?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Marko Burjek</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=buma" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Krizz"><img src="https://avatars0.githubusercontent.com/u/689050?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kristjan</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=Krizz" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/evbarnett"><img src="https://avatars2.githubusercontent.com/u/4960874?v=4?s=100" width="100px;" alt=""/><br /><sub><b>evbarnett</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Aevbarnett" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://www.walkaholic.me"><img src="https://avatars1.githubusercontent.com/u/19690868?v=4?s=100" width="100px;" alt=""/><br /><sub><b>walkaholic.me</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Acarlos-mg89" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://www.webiswhatido.com"><img src="https://avatars1.githubusercontent.com/u/1580910?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Brian Voelker</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Abrianvoe" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://salesking.eu"><img src="https://avatars1.githubusercontent.com/u/13575?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Georg Leciejewski</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Aschorsch" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/cbenz"><img src="https://avatars.githubusercontent.com/u/12686?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Christophe Benz</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Acbenz" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/reyemtm"><img src="https://avatars.githubusercontent.com/u/6398929?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Malcolm Meyer</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/issues?q=author%3Areyemtm" title="Bug reports">🐛</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/jleedev"><img src="https://avatars.githubusercontent.com/u/23022?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Josh Lee</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=jleedev" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/Martin8412"><img src="https://avatars.githubusercontent.com/u/2369612?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Martin Karlsen Jensen</b></sub></a><br /><a href="https://github.com/consbio/mbtileserver/commits?author=Martin8412" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
