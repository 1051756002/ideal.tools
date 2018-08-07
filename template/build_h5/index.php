<?php
    // 调试模式=On, 发布模式=Off
    ini_set('display_errors', 'On');

    include_once substr(__file__, 0, -strlen($_SERVER['PHP_SELF'])) . '/depend/ideal.php';

    // 本地当前URL
    $localUrl = 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF'];
    if (strlen($_SERVER['QUERY_STRING']) > 0) {
        $localUrl .= '?'.$_SERVER['QUERY_STRING'];
    }

    // 当前时间
    $timestamp = time();

    // 验证授权, 如果没有
    validatePermit();

    $accesstoken = getAccessToken($appid, $appsecret);
    $ticket = getTicket($accesstoken);

    // 16位随机数
    $nonceStr = getRadomString(16);
    // 获取signature码
    $signature = sha1("jsapi_ticket=".$ticket."&noncestr=".$nonceStr."&timestamp=".$timestamp."&url=".$localUrl);
?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>@ideal.temp(title)</title>
        <meta name="viewport" content="width=device-width,user-scalable=no,initial-scale=1, minimum-scale=1,maximum-scale=1"/>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="format-detection" content="telephone=no">

        <!-- force webkit on 360 -->
        <meta name="renderer" content="webkit"/>
        <meta name="force-rendering" content="webkit"/>
        <!-- force edge on IE -->
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta name="msapplication-tap-highlight" content="no">

        <!-- force full screen on some browser -->
        <meta name="full-screen" content="yes"/>
        <meta name="x5-fullscreen" content="true"/>
        <meta name="360-fullscreen" content="true"/>

        <!-- force screen orientation on some browser -->
        <meta name="screen-orientation" content="portrait"/>
        <meta name="x5-orientation" content="portrait">
        <meta name="x5-page-mode" content="app">

        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
        <link rel="stylesheet" type="text/css" href="/depend/style-mobile.css"/>
    </head>
    <body>
        <canvas id="GameCanvas" oncontextmenu="event.preventDefault()" tabindex="0"></canvas>
        <div id="splash-wrap">
            <span class="logo"></span>
            <div id="loading-wrap">
                <span id="loading-bar"></span>
                <span id="loading-text">正在加载资源, 请稍后 ...</span>
            </div>
        </div>

        <!-- 项目静态配置 -->
        <script src="src/settings.js" charset="utf-8"></script>

        <!-- 微信SDK -->
        <script src="/depend/jweixin-1.2.0.js"></script>
        <script type="text/javascript">
            wx.config({
                debug: false,
                appId: '<?php echo($appid); ?>',
                timestamp: <?php echo($timestamp); ?>,
                nonceStr: '<?php echo($nonceStr); ?>',
                signature: '<?php echo($signature); ?>',
                jsApiList: [
                    'checkJsApi',
                    'onMenuShareTimeline',
                    'onMenuShareAppMessage',
                    'onMenuShareQQ',
                    'onMenuShareWeibo',
                    'hideMenuItems',
                    'showMenuItems',
                    'hideAllNonBaseMenuItem',
                    'showAllNonBaseMenuItem',
                    'translateVoice',
                    'startRecord',
                    'stopRecord',
                    'onRecordEnd',
                    'playVoice',
                    'pauseVoice',
                    'stopVoice',
                    'uploadVoice',
                    'downloadVoice',
                    'chooseImage',
                    'openAddress',
                    'previewImage',
                    'uploadImage',
                    'downloadImage',
                    'getNetworkType',
                    'openLocation',
                    'getLocation',
                    'hideOptionMenu',
                    'showOptionMenu',
                    'closeWindow',
                    'scanQRCode',
                    'chooseWXPay',
                    'openProductSpecificView',
                    'addCard',
                    'chooseCard',
                    'openCard',
                ]
            });

            wx.ready(function() {
                var localUrl = location.origin + location.pathname;

                // 隐藏所有非基础按钮接口
                wx.hideAllNonBaseMenuItem();

                // 分享给朋友
                wx.onMenuShareAppMessage({
                    title: '爱摩罗棋牌',
                    desc: '爱摩罗棋牌，精彩只为等你来！快来一起玩爱摩罗棋牌吧！',
                    link: localUrl,
                    type: 'link',
                    imgUrl: 'http://h5.xingdong.co/depend/favicon.png',
                });

                // 显示功能按钮接口
                wx.showMenuItems({
                    menuList: ['menuItem:share:appMessage', 'menuItem:favorite']
                });
            });
        </script>

        <!-- 游戏入口 -->
        <script src="main.js" charset="utf-8"></script>

        @ideal.define(EnableEruda)
        <!-- 调试齿轮 -->
        <script src="/depend/eruda.min.js"></script>
        <script type="text/javascript">
            eruda.init();
            eruda.get('console').config.set('displayUnenumerable', false);  // fix #6365
        </script>
        @ideal.undef

        <!-- 剪切板 -->
        <script src="/depend/clipboard.min.js"></script>
    </body>
</html>
