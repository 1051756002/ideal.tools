(function() {
    if (!location.pathname.endsWith('.php')) {
        var pathname;
        if (location.pathname.endsWith('/')) {
            pathname = location.pathname + 'index.php';
        } else {
            pathname = location.pathname + '/index.php';
        }
        location.href = location.origin + pathname + location.search;
    }
})();

(function() {
    function rnd(min, max) {
        if (typeof max == 'undefined') { max = min; min = 0; }
        return Math.floor(Math.random() * max + min);
    };

    function orientation() {
        var br = document.body.getClientRects()[0];
        return br.width > br.height ? 'landscape': 'portrait';
    };

    var displayText = '正在加载, 请稍后...';
    var nowTime = Date.now();
    var progress = 0;
    var bar = document.getElementById('loading-bar');
    var wrap = document.getElementById('loading-wrap');
    var text = document.getElementById('loading-text');

    var siid = setInterval(function() {
        var barRect = bar.getClientRects()[0];
        var wrapRect = wrap.getClientRects()[0];
        var present, limit;
        if (orientation() == 'landscape') {
            present = barRect.width;
            limit = wrapRect.width;
        } else {
            present = barRect.height;
            limit = wrapRect.height;
        }
        // 小于35%
        if (present < limit * 0.35) {
            progress = present + rnd(limit * 0.05);
        }
        // 小于60%
        else if (present < limit * 0.6) {
            progress = present + rnd(limit * 0.02);
        }
        // 小于95%
        else if (present < limit * 0.95) {
            progress = present + rnd(limit * 0.01);
        }
        else {
            clearInterval(siid);
            console.log('Logo耗时%s秒', (Date.now() - nowTime) / 1000);
        }
        bar.style.width = progress + 'px';
        text.innerHTML = displayText + ' (' + Math.floor((progress / limit) * 100) + '%)';
    }, 20);

    function complete() {
        clearInterval(siid);
        bar.style.width = '300px';
        text.innerHTML = displayText + ' (100%)';
        removeEventListener('splash.complete', complete);
    };
    addEventListener('splash.complete', complete, false);
})();

(function() {

    'use strict';

    function boot() {

        var settings = window._CCSettings;
        window._CCSettings = undefined;

        if (!settings.debug) {
            var uuids = settings.uuids;

            var rawAssets = settings.rawAssets;
            var assetTypes = settings.assetTypes;
            var realRawAssets = settings.rawAssets = {};
            for (var mount in rawAssets) {
                var entries = rawAssets[mount];
                var realEntries = realRawAssets[mount] = {};
                for (var id in entries) {
                    var entry = entries[id];
                    var type = entry[1];
                    // retrieve minified raw asset
                    if (typeof type === 'number') {
                        entry[1] = assetTypes[type];
                    }
                    // retrieve uuid
                    realEntries[uuids[id] || id] = entry;
                }
            }

            var scenes = settings.scenes;
            for (var i = 0; i < scenes.length; ++i) {
                var scene = scenes[i];
                if (typeof scene.uuid === 'number') {
                    scene.uuid = uuids[scene.uuid];
                }
            }

            var packedAssets = settings.packedAssets;
            for (var packId in packedAssets) {
                var packedIds = packedAssets[packId];
                for (var j = 0; j < packedIds.length; ++j) {
                    if (typeof packedIds[j] === 'number') {
                        packedIds[j] = uuids[packedIds[j]];
                    }
                }
            }
        }

        var canvas;

        if (cc.sys.isBrowser) {
            canvas = document.getElementById('GameCanvas');
        }

        function setLoadingDisplay() {
            var splash = document.getElementById('splash-wrap');
            cc.director.once(cc.Director.EVENT_AFTER_SCENE_LAUNCH, function() {
                var t = Date.now();
                var SHOW_TIME = 1500;
                var FADE_TIME = 500;
                var FRAME_TIME = 16;

                var fn = function() {
                    var dt = Date.now() - t;
                    if (dt < SHOW_TIME) {
                        setTimeout(fn, FRAME_TIME);
                    } else {
                        var op = 1 - ((dt - SHOW_TIME) / FADE_TIME);
                        if (op < 0) {
                            splash.style.opacity = 0;
                            splash.style.display = 'none';
                            canvas.style.opacity = 1;
                        } else {
                            splash.style.opacity = op;
                            canvas.style.opacity = 1 - op;
                            setTimeout(fn, FRAME_TIME);
                        }
                    }
                };
                setTimeout(fn, FRAME_TIME);
            });
            dispatchEvent(new Event('splash.complete'));
        }

        var onStart = function() {
            cc.view.resizeWithBrowserSize(true);

            // UC browser on many android devices have performance issue with retina display
            if (cc.sys.os !== cc.sys.OS_ANDROID || cc.sys.browserType !== cc.sys.BROWSER_TYPE_UC) {
                cc.view.enableRetina(true);
            }
            if (cc.sys.isBrowser) {
                setLoadingDisplay();
            }

            if (cc.sys.isMobile) {
                if (settings.orientation === 'landscape') {
                    cc.view.setOrientation(cc.macro.ORIENTATION_LANDSCAPE);
                } else if (settings.orientation === 'portrait') {
                    cc.view.setOrientation(cc.macro.ORIENTATION_PORTRAIT);
                }
            }

            if (cc.sys.isBrowser && cc.sys.os === cc.sys.OS_ANDROID) {
                cc.macro.DOWNLOAD_MAX_CONCURRENT = 2;
            }

            cc.AssetLibrary.init({
                libraryPath: 'res/import',
                rawAssetsBase: 'res/raw-',
                rawAssets: settings.rawAssets,
                packedAssets: settings.packedAssets,
                md5AssetsMap: settings.md5AssetsMap
            });

            var launchScene = settings.launchScene;
            cc.director.loadScene(launchScene, null,
                function() {
                    if (cc.sys.isBrowser) {
                        // show canvas
                        canvas.style.visibility = '';
                        var div = document.getElementById('GameDiv');
                        if (div) {
                            div.style.backgroundImage = '';
                        }
                    }
                    cc.loader.onProgress = null;
                    console.log('Success to load scene: ' + launchScene);
                }
            );
        };

        var jsList = settings.jsList;
        var bundledScript = 'src/project.js';
        if (jsList) {
            jsList = jsList.map(function(x) {
                return 'src/' + x;
            });
            jsList.push(bundledScript);
        } else {
            jsList = [bundledScript];
        }

        jsList = jsList.map(function(x) {
            return x + '?_t=' + Date.now();
        });

        var option = {
            id: 'GameCanvas',
            scenes: settings.scenes,
            debugMode: settings.debug ? cc.DebugMode.INFO : cc.DebugMode.ERROR,
            showFPS: settings.debug,
            frameRate: 60,
            jsList: jsList,
            groupList: settings.groupList,
            collisionMatrix: settings.collisionMatrix,
            renderMode: 0
        };

        cc.game.run(option, onStart);
    }

    var cocos2d = document.createElement('script');
    cocos2d.async = true;
    cocos2d.src = '/depend/cocos2d-js-min.js?v=@ideal.code(%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%)';

    var engineLoaded = function() {
        document.body.removeChild(cocos2d);
        cocos2d.removeEventListener('load', engineLoaded, false);
        boot();
    };
    cocos2d.addEventListener('load', engineLoaded, false);
    document.body.appendChild(cocos2d);
})();
