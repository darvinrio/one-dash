(function() {
  var fn = function() {
    
    (function(root) {
      function now() {
        return new Date();
      }
    
      var force = false;
    
      if (typeof root._bokeh_onload_callbacks === "undefined" || force === true) {
        root._bokeh_onload_callbacks = [];
        root._bokeh_is_loading = undefined;
      }
    
      
      
    
      var element = document.getElementById("55c6ca53-a4d0-4faf-9fdf-353847d77e0f");
        if (element == null) {
          console.warn("Bokeh: autoload.js configured with elementid '55c6ca53-a4d0-4faf-9fdf-353847d77e0f' but no matching script tag was found.")
        }
      
    
      function run_callbacks() {
        try {
          root._bokeh_onload_callbacks.forEach(function(callback) {
            if (callback != null)
              callback();
          });
        } finally {
          delete root._bokeh_onload_callbacks
        }
        console.debug("Bokeh: all callbacks have finished");
      }
    
      function load_libs(css_urls, js_urls, callback) {
        if (css_urls == null) css_urls = [];
        if (js_urls == null) js_urls = [];
    
        root._bokeh_onload_callbacks.push(callback);
        if (root._bokeh_is_loading > 0) {
          console.debug("Bokeh: BokehJS is being loaded, scheduling callback at", now());
          return null;
        }
        if (js_urls == null || js_urls.length === 0) {
          run_callbacks();
          return null;
        }
        console.debug("Bokeh: BokehJS not loaded, scheduling load and callback at", now());
        root._bokeh_is_loading = css_urls.length + js_urls.length;
    
        function on_load() {
          root._bokeh_is_loading--;
          if (root._bokeh_is_loading === 0) {
            console.debug("Bokeh: all BokehJS libraries/stylesheets loaded");
            run_callbacks()
          }
        }
    
        function on_error(url) {
          console.error("failed to load " + url);
        }
    
        for (let i = 0; i < css_urls.length; i++) {
          const url = css_urls[i];
          const element = document.createElement("link");
          element.onload = on_load;
          element.onerror = on_error.bind(null, url);
          element.rel = "stylesheet";
          element.type = "text/css";
          element.href = url;
          console.debug("Bokeh: injecting link tag for BokehJS stylesheet: ", url);
          document.body.appendChild(element);
        }
    
        const hashes = {"https://cdn.bokeh.org/bokeh/release/bokeh-2.3.3.min.js": "dM3QQsP+wXdHg42wTqW85BjZQdLNNIXqlPw/BgKoExPmTG7ZLML4EGqLMfqHT6ON", "https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.3.3.min.js": "8x57I4YuIfu8XyZfFo0XVr2WAT8EK4rh/uDe3wF7YuW2FNUSNEpJbsPaB1nJ2fz2", "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.3.3.min.js": "3QTqdz9LyAm2i0sG5XTePsHec3UHWwVsrOL68SYRoAXsafvfAyqtQ+h440+qIBhS"};
    
        for (let i = 0; i < js_urls.length; i++) {
          const url = js_urls[i];
          const element = document.createElement('script');
          element.onload = on_load;
          element.onerror = on_error.bind(null, url);
          element.async = false;
          element.src = url;
          if (url in hashes) {
            element.crossOrigin = "anonymous";
            element.integrity = "sha384-" + hashes[url];
          }
          console.debug("Bokeh: injecting script tag for BokehJS library: ", url);
          document.head.appendChild(element);
        }
      };
    
      function inject_raw_css(css) {
        const element = document.createElement("style");
        element.appendChild(document.createTextNode(css));
        document.body.appendChild(element);
      }
    
      
      var js_urls = ["https://cdn.bokeh.org/bokeh/release/bokeh-2.3.3.min.js", "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-2.3.3.min.js", "https://cdn.bokeh.org/bokeh/release/bokeh-tables-2.3.3.min.js"];
      var css_urls = [];
      
    
      var inline_js = [
        function(Bokeh) {
          Bokeh.set_log_level("info");
        },
        
        function(Bokeh) {
          (function() {
            var fn = function() {
              Bokeh.safely(function() {
                (function(root) {
                  function embed_document(root) {
                    
                  var docs_json = '{"c5ec0337-6932-486f-b3c2-da423db553ff":{"defs":[],"roots":{"references":[{"attributes":{"dimensions":"width"},"id":"1019","type":"WheelZoomTool"},{"attributes":{"months":[0,4,8]},"id":"1058","type":"MonthsTicker"},{"attributes":{"num_minor_ticks":5,"tickers":[{"id":"1049"},{"id":"1050"},{"id":"1051"},{"id":"1052"},{"id":"1053"},{"id":"1054"},{"id":"1055"},{"id":"1056"},{"id":"1057"},{"id":"1058"},{"id":"1059"},{"id":"1060"}]},"id":"1012","type":"DatetimeTicker"},{"attributes":{"callback":{"id":"1035"},"formatters":{"@BLOCK_HOUR":"datetime"},"mode":"vline","show_arrow":false,"tooltips":"\\n        &lt;div&gt;\\n        &lt;h3&gt; @TOTAL_LIQUIDITY_STR &lt;/h3&gt;\\n        &lt;h7&gt; @DATE_STR &lt;/h7&gt;\\n        &lt;/div&gt;\\n        "},"id":"1036","type":"HoverTool"},{"attributes":{"axis":{"id":"1011"},"ticker":null,"visible":false},"id":"1014","type":"Grid"},{"attributes":{},"id":"1047","type":"Selection"},{"attributes":{},"id":"1022","type":"ResetTool"},{"attributes":{"args":{"p":{"id":"1002"}},"code":"\\n        var tooltips = document.getElementsByClassName(\\"bk-tooltip\\");\\n        const tw = 100;\\n        for (var i = 0; i &lt; tooltips.length; i++) {\\n            tooltips[i].style.top = &#x27;10px&#x27;; \\n            tooltips[i].style.left = p.width/8 - tw/2 + &#x27;px&#x27;; \\n            tooltips[i].style.width = tw + &#x27;px&#x27;; \\n        } "},"id":"1035","type":"CustomJS"},{"attributes":{},"id":"1039","type":"Title"},{"attributes":{},"id":"1005","type":"DataRange1d"},{"attributes":{},"id":"1048","type":"UnionRenderers"},{"attributes":{"axis_label":"Time","formatter":{"id":"1046"},"major_label_policy":{"id":"1044"},"ticker":{"id":"1012"}},"id":"1011","type":"DatetimeAxis"},{"attributes":{"axis":{"id":"1015"},"dimension":1,"ticker":null,"visible":false},"id":"1018","type":"Grid"},{"attributes":{"dimensions":"height"},"id":"1020","type":"WheelZoomTool"},{"attributes":{"dimensions":"width"},"id":"1021","type":"PanTool"},{"attributes":{"source":{"id":"1028"}},"id":"1033","type":"CDSView"},{"attributes":{},"id":"1041","type":"AllLabels"},{"attributes":{},"id":"1003","type":"DataRange1d"},{"attributes":{"dimensions":"height","line_alpha":0.5},"id":"1034","type":"CrosshairTool"},{"attributes":{"axis_label":"TVL_USD","formatter":{"id":"1043"},"major_label_policy":{"id":"1041"},"ticker":{"id":"1016"},"visible":false},"id":"1015","type":"LinearAxis"},{"attributes":{"line_alpha":0.1,"line_color":"#fc077d","line_width":2,"x":{"field":"BLOCK_HOUR"},"y":{"field":"TOTAL_LIQUIDITY_USD"}},"id":"1031","type":"Line"},{"attributes":{"mantissas":[1,2,5],"max_interval":500.0,"num_minor_ticks":0},"id":"1049","type":"AdaptiveTicker"},{"attributes":{},"id":"1043","type":"BasicTickFormatter"},{"attributes":{"data_source":{"id":"1028"},"glyph":{"id":"1030"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"1031"},"view":{"id":"1033"}},"id":"1032","type":"GlyphRenderer"},{"attributes":{"base":60,"mantissas":[1,2,5,10,15,20,30],"max_interval":1800000.0,"min_interval":1000.0,"num_minor_ticks":0},"id":"1050","type":"AdaptiveTicker"},{"attributes":{},"id":"1016","type":"BasicTicker"},{"attributes":{},"id":"1060","type":"YearsTicker"},{"attributes":{"data":{"BLOCK_HOUR":{"__ndarray__":"AADAaJLDd0IAAAADQMN3QgAAQJ3twndCAACAN5vCd0IAAMDRSMJ3QgAAAGz2wXdCAABABqTBd0IAAICgUcF3QgAAwDr/wHdCAAAA1azAd0IAAEBvWsB3QgAAgAkIwHdCAADAo7W/d0IAAAA+Y793QgAAQNgQv3dCAACAcr6+d0IAAMAMbL53QgAAAKcZvndCAABAQce9d0IAAIDbdL13QgAAwHUivXdCAAAAENC8d0IAAECqfbx3QgAAgEQrvHdCAADA3ti7d0IAAAB5hrt3QgAAQBM0u3dCAACAreG6d0IAAMBHj7p3QgAAAOI8undCAABAfOq5d0IAAIAWmLl3QgAAwLBFuXdCAAAAS/O4d0IAAEDloLh3QgAAgH9OuHdCAADAGfy3d0IAAAC0qbd3QgAAQE5Xt3dCAACA6AS3d0IAAMCCsrZ3QgAAAB1gtndCAABAtw22d0IAAIBRu7V3QgAAwOtotXdCAAAAhha1d0IAAEAgxLR3QgAAgLpxtHdCAADAVB+0d0IAAADvzLN3QgAAQIl6s3dCAACAIyizd0IAAMC91bJ3QgAAAFiDsndCAABA8jCyd0IAAICM3rF3QgAAwCaMsXdCAAAAwTmxd0IAAEBb57B3QgAAgPWUsHdCAADAj0Kwd0IAAAAq8K93QgAAQMSdr3dCAACAXkuvd0IAAMD4+K53QgAAAJOmrndCAABALVSud0IAAIDHAa53QgAAwGGvrXdCAAAA/Fytd0IAAECWCq13QgAAgDC4rHdCAADAymWsd0IAAABlE6x3QgAAQP/Aq3dCAACAmW6rd0IAAMAzHKt3QgAAAM7JqndCAABAaHeqd0IAAIACJap3QgAAwJzSqXdCAAAAN4Cpd0IAAEDRLal3QgAAgGvbqHdCAADABYmod0IAAACgNqh3QgAAQDrkp3dCAACA1JGnd0IAAMBuP6d3QgAAAAntpndCAABAo5qmd0IAAIA9SKZ3QgAAwNf1pXdCAAAAcqOld0IAAEAMUaV3QgAAgKb+pHdCAADAQKykd0IAAADbWaR3QgAAQHUHpHdCAACAD7Wjd0IAAMCpYqN3QgAAAEQQo3dCAABA3r2id0IAAIB4a6J3QgAAwBIZondCAAAArcahd0IAAEBHdKF3QgAAgOEhoXdCAADAe8+gd0IAAAAWfaB3QgAAQLAqoHdCAACAStifd0IAAMDkhZ93QgAAAH8zn3dCAABAGeGed0IAAICzjp53QgAAwE08nndCAAAA6Omdd0IAAECCl513QgAAgBxFnXdCAADAtvKcd0IAAABRoJx3QgAAQOtNnHdCAACAhfubd0IAAMAfqZt3QgAAALpWm3dCAABAVASbd0IAAIDusZp3QgAAwIhfmndCAAAAIw2ad0IAAEC9upl3QgAAgFdomXdCAADA8RWZd0IAAACMw5h3QgAAQCZxmHdCAACAwB6Yd0IAAMBazJd3QgAAAPV5l3dCAABAjyeXd0IAAIAp1ZZ3QgAAwMOClndCAAAAXjCWd0IAAED43ZV3QgAAgJKLlXdCAADALDmVd0IAAADH5pR3QgAAQGGUlHdCAACA+0GUd0IAAMCV75N3QgAAADCdk3dCAABAykqTd0I=","dtype":"float64","order":"little","shape":[151]},"DATE_STR":["Oct 01, 2021","Sep 30, 2021","Sep 29, 2021","Sep 28, 2021","Sep 27, 2021","Sep 26, 2021","Sep 25, 2021","Sep 24, 2021","Sep 23, 2021","Sep 22, 2021","Sep 21, 2021","Sep 20, 2021","Sep 19, 2021","Sep 18, 2021","Sep 17, 2021","Sep 16, 2021","Sep 15, 2021","Sep 14, 2021","Sep 13, 2021","Sep 12, 2021","Sep 11, 2021","Sep 10, 2021","Sep 09, 2021","Sep 08, 2021","Sep 07, 2021","Sep 06, 2021","Sep 05, 2021","Sep 04, 2021","Sep 03, 2021","Sep 02, 2021","Sep 01, 2021","Aug 31, 2021","Aug 30, 2021","Aug 29, 2021","Aug 28, 2021","Aug 27, 2021","Aug 26, 2021","Aug 25, 2021","Aug 24, 2021","Aug 23, 2021","Aug 22, 2021","Aug 21, 2021","Aug 20, 2021","Aug 19, 2021","Aug 18, 2021","Aug 17, 2021","Aug 16, 2021","Aug 15, 2021","Aug 14, 2021","Aug 13, 2021","Aug 12, 2021","Aug 11, 2021","Aug 10, 2021","Aug 09, 2021","Aug 08, 2021","Aug 07, 2021","Aug 06, 2021","Aug 05, 2021","Aug 04, 2021","Aug 03, 2021","Aug 02, 2021","Aug 01, 2021","Jul 31, 2021","Jul 30, 2021","Jul 29, 2021","Jul 28, 2021","Jul 27, 2021","Jul 26, 2021","Jul 25, 2021","Jul 24, 2021","Jul 23, 2021","Jul 22, 2021","Jul 21, 2021","Jul 20, 2021","Jul 19, 2021","Jul 18, 2021","Jul 17, 2021","Jul 16, 2021","Jul 15, 2021","Jul 14, 2021","Jul 13, 2021","Jul 12, 2021","Jul 11, 2021","Jul 10, 2021","Jul 09, 2021","Jul 08, 2021","Jul 07, 2021","Jul 06, 2021","Jul 05, 2021","Jul 04, 2021","Jul 03, 2021","Jul 02, 2021","Jul 01, 2021","Jun 30, 2021","Jun 29, 2021","Jun 28, 2021","Jun 27, 2021","Jun 26, 2021","Jun 25, 2021","Jun 24, 2021","Jun 23, 2021","Jun 22, 2021","Jun 21, 2021","Jun 20, 2021","Jun 19, 2021","Jun 18, 2021","Jun 17, 2021","Jun 16, 2021","Jun 15, 2021","Jun 14, 2021","Jun 13, 2021","Jun 12, 2021","Jun 11, 2021","Jun 10, 2021","Jun 09, 2021","Jun 08, 2021","Jun 07, 2021","Jun 06, 2021","Jun 05, 2021","Jun 04, 2021","Jun 03, 2021","Jun 02, 2021","Jun 01, 2021","May 31, 2021","May 30, 2021","May 29, 2021","May 28, 2021","May 27, 2021","May 26, 2021","May 25, 2021","May 24, 2021","May 23, 2021","May 22, 2021","May 21, 2021","May 20, 2021","May 19, 2021","May 18, 2021","May 17, 2021","May 16, 2021","May 15, 2021","May 14, 2021","May 13, 2021","May 12, 2021","May 11, 2021","May 10, 2021","May 09, 2021","May 08, 2021","May 07, 2021","May 06, 2021","May 05, 2021","May 04, 2021"],"TOTAL_LIQUIDITY_STR":["$2.24B","$2.28B","$2.3B","$2.26B","$2.55B","$2.27B","$2.31B","$2.36B","$2.27B","$2.24B","$2.19B","$2.71B","$2.42B","$2.38B","$2.44B","$2.35B","$2.33B","$2.19B","$2.43B","$2.25B","$2.17B","$2.6B","$2.29B","$2.53B","$2.5B","$2.94B","$2.76B","$2.7B","$2.68B","$2.71B","$2.61B","$2.73B","$2.71B","$2.69B","$2.68B","$2.6B","$2.69B","$2.7B","$2.7B","$2.83B","$2.63B","$2.61B","$2.6B","$2.39B","$2.31B","$2.35B","$2.41B","$2.39B","$2.38B","$2.21B","$2.2B","$2.21B","$2.13B","$2.07B","$2.3B","$2.15B","$2.09B","$1.92B","$1.99B","$2.1B","$1.94B","$2.02B","$1.94B","$1.94B","$1.86B","$1.8B","$1.77B","$1.82B","$1.84B","$1.65B","$1.71B","$1.61B","$1.58B","$1.63B","$1.57B","$1.74B","$1.51B","$1.54B","$1.59B","$1.95B","$1.56B","$1.69B","$1.58B","$1.64B","$1.58B","$1.67B","$1.71B","$1.66B","$1.78B","$1.69B","$1.61B","$1.65B","$1.7B","$2.07B","$1.58B","$1.5B","$1.43B","$1.49B","$1.6B","$1.49B","$1.48B","$1.46B","$1.62B","$1.85B","$2.08B","$1.72B","$1.7B","$1.77B","$1.81B","$1.73B","$1.78B","$1.64B","$1.71B","$1.81B","$1.74B","$1.76B","$1.81B","$2.13B","$2.02B","$1.95B","$2.07B","$1.77B","$1.83B","$1.69B","$1.74B","$1.58B","$1.65B","$1.59B","$1.54B","$1.47B","$1.16B","$1.05B","$1.04B","$1.11B","$1.01B","$1.14B","$1.12B","$1.15B","$1.04B","$1.1B","$972.4M","$992.18M","$944.96M","$757.45M","$650.07M","$649.01M","$614.66M","$567.44M","$404.84M","$145.18M","$165.5K"],"TOTAL_LIQUIDITY_USD":{"__ndarray__":"M6VRTZqz4EFRi6pvngLhQSIiUA6PH+FBG/q9sSvW4EHyTlup/gLjQQSNVpbB6+BBgkvcBNU64UHD2K7RuY3hQQyHhNk54+BBBoIXERGs4EFokHxJAkngQZzT3/axOORB/tWtgjMN4kG1+wfKi7zhQX0V6BeIJ+JB+WynKRl74UFpxWLZ3lPhQeaHZ6g3TeBBnJcdUa8Z4kFF2lP25MjgQbpzi4rHJuBBTTz/6cRi40FbPgI6yQ7hQeBrNisY1uJBOXbRbmul4kEvhH79SPDlQYmWMPFPleRB0sQBJa0j5EGc0/7O/PHjQeupRP/mLuRBeugIzRp040HaF/FvYlvkQTEynxbrOeRBFQ82NUMT5EFQcxT9x/fjQTn6nliZZ+NBzOdkGKIJ5EHuw7A8ZhvkQUR9I5poHeRBU5mKR0cc5UF6rCPaBo/jQTn1hQ0oc+NBjH5VEnZd40F+WMzIdNThQeOhPj/BNOFBMJHHRz5+4UHWk+xfxO3hQVbbbIto1OFBRzuUpRu04UF/y80Jb3jgQeFjfbnRY+BBV3OyECNv4EEqlm/VQsvfQWd4VpEz3N5B5aEr4Eoc4UEVgWtypAngQS+zzeTKH99BYNoYosyp3EHMC3by0bDdQQsgiNt9Wd9BGGjo1cDq3EEoRarSQQfeQcMK+5W849xBbut7CNDw3EEvZ5OI/b/bQSubFExvzNpB0IRnebdm2kEZEdbMwxPbQQrQlKLhWdtBvzRd/8eQ2EEr5wkrVIHZQY4lIs1Y9tdBd06676p910Hj4s1HzDjYQR4AmyRJW9dBMiBib2n42UF5XLEHcX7WQbfWRTJn6NZBSzIoF5bA10F03AICkRDdQZUJtzsCR9dBkqHBQpQ62UEOD7pjNprXQdEoxeSledhBBScyhaqC10FqY4g1Z9TYQShmVokqg9lBmamrpoe22EFoghCeSHnaQTZDnODMLtlBbdqI2On610HHccLHdaDYQXfsT82wUtlBG74HKI3c3kFF7LCaBJbXQQ9OsICoSNZBsA71A2I/1UHWkqPpdzbWQZIzCCMY59dBKH0D278w1kGmAZxqBRHWQcBB7WqQrtVBJ5F0e1I12EEBT6/w5IzbQfUspn4rAd9BcDwhjv+X2UFXQc1JfmbZQYmM/NwEZdpBLpptjI382kFIUBE/ErvZQZFFs8sgiNpBLTkMjjRl2EFL5/gDW4nZQbABTRyV9dpBV77fyFb22UESWOtDnEHaQbG9qGXVANtBeAoicJDG30GFtL31ihLeQYdEBEwDAN1B/qKbBS3Z3kHOsIZ2YGraQRlLQEzYRNtBe9SA8uc42UFMNGmGk+7ZQc+6lAWQitdBWxmichaO2EFb1+18cbjXQYkRlTcK7dZB7zAXiZzt1UH2NQGNQFPRQRiCTztzRc9Bpm67RKoZz0G5h8kPOorQQS8ubGJT9M1BRG2yn4X80EFF9scBkrTQQRU23jkSGNFBNxqtWfH5zkEtcyppumXQQXl7JEPT+sxBGyrST7mRzUGBusB/finMQZge3WLbksZBdagd5Z5fw0EXx/chlVfDQeqP4mp8UcJB/irZpkHpwEHMLLtFbyG4Qbk0oi+BTqFBGuaYduEzBEE=","dtype":"float64","order":"little","shape":[151]},"index":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150]},"selected":{"id":"1047"},"selection_policy":{"id":"1048"}},"id":"1028","type":"ColumnDataSource"},{"attributes":{},"id":"1046","type":"DatetimeTickFormatter"},{"attributes":{"base":24,"mantissas":[1,2,4,6,8,12],"max_interval":43200000.0,"min_interval":3600000.0,"num_minor_ticks":0},"id":"1051","type":"AdaptiveTicker"},{"attributes":{"months":[0,1,2,3,4,5,6,7,8,9,10,11]},"id":"1056","type":"MonthsTicker"},{"attributes":{},"id":"1044","type":"AllLabels"},{"attributes":{},"id":"1007","type":"LinearScale"},{"attributes":{"days":[1,15]},"id":"1055","type":"DaysTicker"},{"attributes":{"days":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]},"id":"1052","type":"DaysTicker"},{"attributes":{"days":[1,4,7,10,13,16,19,22,25,28]},"id":"1053","type":"DaysTicker"},{"attributes":{},"id":"1009","type":"LinearScale"},{"attributes":{"days":[1,8,15,22]},"id":"1054","type":"DaysTicker"},{"attributes":{"months":[0,6]},"id":"1059","type":"MonthsTicker"},{"attributes":{"months":[0,2,4,6,8,10]},"id":"1057","type":"MonthsTicker"},{"attributes":{"below":[{"id":"1011"}],"center":[{"id":"1014"},{"id":"1018"}],"height":300,"left":[{"id":"1015"}],"outline_line_color":null,"renderers":[{"id":"1032"}],"sizing_mode":"stretch_width","title":{"id":"1039"},"toolbar":{"id":"1023"},"x_range":{"id":"1003"},"x_scale":{"id":"1007"},"y_range":{"id":"1005"},"y_scale":{"id":"1009"}},"id":"1002","subtype":"Figure","type":"Plot"},{"attributes":{"active_multi":null,"tools":[{"id":"1019"},{"id":"1020"},{"id":"1021"},{"id":"1022"},{"id":"1036"},{"id":"1034"}]},"id":"1023","type":"Toolbar"},{"attributes":{"line_color":"#fc077d","line_width":2,"x":{"field":"BLOCK_HOUR"},"y":{"field":"TOTAL_LIQUIDITY_USD"}},"id":"1030","type":"Line"}],"root_ids":["1002"]},"title":"Bokeh Application","version":"2.3.3"}}';
                  var render_items = [{"docid":"c5ec0337-6932-486f-b3c2-da423db553ff","root_ids":["1002"],"roots":{"1002":"55c6ca53-a4d0-4faf-9fdf-353847d77e0f"}}];
                  root.Bokeh.embed.embed_items(docs_json, render_items);
                
                  }
                  if (root.Bokeh !== undefined) {
                    embed_document(root);
                  } else {
                    var attempts = 0;
                    var timer = setInterval(function(root) {
                      if (root.Bokeh !== undefined) {
                        clearInterval(timer);
                        embed_document(root);
                      } else {
                        attempts++;
                        if (attempts > 100) {
                          clearInterval(timer);
                          console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                        }
                      }
                    }, 10, root)
                  }
                })(window);
              });
            };
            if (document.readyState != "loading") fn();
            else document.addEventListener("DOMContentLoaded", fn);
          })();
        },
        function(Bokeh) {
        
        
        }
      ];
    
      function run_inline_js() {
        
        for (var i = 0; i < inline_js.length; i++) {
          inline_js[i].call(root, root.Bokeh);
        }
        
      }
    
      if (root._bokeh_is_loading === 0) {
        console.debug("Bokeh: BokehJS loaded, going straight to plotting");
        run_inline_js();
      } else {
        load_libs(css_urls, js_urls, function() {
          console.debug("Bokeh: BokehJS plotting callback run at", now());
          run_inline_js();
        });
      }
    }(window));
  };
  if (document.readyState != "loading") fn();
  else document.addEventListener("DOMContentLoaded", fn);
})();