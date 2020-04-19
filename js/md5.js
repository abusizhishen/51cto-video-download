MD5 = function(e) {
            var t, a = 0, n = 8;
            function o(e, t, r, i, a, n) {
                return g((s = g(g(t, e), g(i, n))) << a | s >>> 32 - a, r);
                var s
            }
            function c(e, t, r, i, a, n, s) {
                return o(t & r | ~t & i, e, t, a, n, s)
            }
            function h(e, t, r, i, a, n, s) {
                return o(t & i | r & ~i, e, t, a, n, s)
            }
            function f(e, t, r, i, a, n, s) {
                return o(t ^ r ^ i, e, t, a, n, s)
            }
            function p(e, t, r, i, a, n, s) {
                return o(r ^ (t | ~i), e, t, a, n, s)
            }
            function g(e, t) {
                var r = (65535 & e) + (65535 & t);
                return (e >> 16) + (t >> 16) + (r >> 16) << 16 | 65535 & r
            }
            return function(e) {
                for (var t = a ? "0123456789ABCDEF" : "0123456789abcdef", r = "", i = 0; i < 4 * e.length; i++)
                    r += t.charAt(e[i >> 2] >> i % 4 * 8 + 4 & 15) + t.charAt(e[i >> 2] >> i % 4 * 8 & 15);
                return r
            }(function(e, t) {
                e[t >> 5] |= 128 << t % 32,
                e[14 + (t + 64 >>> 9 << 4)] = t;
                for (var r = 1732584193, i = -271733879, a = -1732584194, n = 271733878, s = 0; s < e.length; s += 16) {
                    var o = r
                      , l = i
                      , u = a
                      , d = n;
                    i = p(i = p(i = p(i = p(i = f(i = f(i = f(i = f(i = h(i = h(i = h(i = h(i = c(i = c(i = c(i = c(i, a = c(a, n = c(n, r = c(r, i, a, n, e[s + 0], 7, -680876936), i, a, e[s + 1], 12, -389564586), r, i, e[s + 2], 17, 606105819), n, r, e[s + 3], 22, -1044525330), a = c(a, n = c(n, r = c(r, i, a, n, e[s + 4], 7, -176418897), i, a, e[s + 5], 12, 1200080426), r, i, e[s + 6], 17, -1473231341), n, r, e[s + 7], 22, -45705983), a = c(a, n = c(n, r = c(r, i, a, n, e[s + 8], 7, 1770035416), i, a, e[s + 9], 12, -1958414417), r, i, e[s + 10], 17, -42063), n, r, e[s + 11], 22, -1990404162), a = c(a, n = c(n, r = c(r, i, a, n, e[s + 12], 7, 1804603682), i, a, e[s + 13], 12, -40341101), r, i, e[s + 14], 17, -1502002290), n, r, e[s + 15], 22, 1236535329), a = h(a, n = h(n, r = h(r, i, a, n, e[s + 1], 5, -165796510), i, a, e[s + 6], 9, -1069501632), r, i, e[s + 11], 14, 643717713), n, r, e[s + 0], 20, -373897302), a = h(a, n = h(n, r = h(r, i, a, n, e[s + 5], 5, -701558691), i, a, e[s + 10], 9, 38016083), r, i, e[s + 15], 14, -660478335), n, r, e[s + 4], 20, -405537848), a = h(a, n = h(n, r = h(r, i, a, n, e[s + 9], 5, 568446438), i, a, e[s + 14], 9, -1019803690), r, i, e[s + 3], 14, -187363961), n, r, e[s + 8], 20, 1163531501), a = h(a, n = h(n, r = h(r, i, a, n, e[s + 13], 5, -1444681467), i, a, e[s + 2], 9, -51403784), r, i, e[s + 7], 14, 1735328473), n, r, e[s + 12], 20, -1926607734), a = f(a, n = f(n, r = f(r, i, a, n, e[s + 5], 4, -378558), i, a, e[s + 8], 11, -2022574463), r, i, e[s + 11], 16, 1839030562), n, r, e[s + 14], 23, -35309556), a = f(a, n = f(n, r = f(r, i, a, n, e[s + 1], 4, -1530992060), i, a, e[s + 4], 11, 1272893353), r, i, e[s + 7], 16, -155497632), n, r, e[s + 10], 23, -1094730640), a = f(a, n = f(n, r = f(r, i, a, n, e[s + 13], 4, 681279174), i, a, e[s + 0], 11, -358537222), r, i, e[s + 3], 16, -722521979), n, r, e[s + 6], 23, 76029189), a = f(a, n = f(n, r = f(r, i, a, n, e[s + 9], 4, -640364487), i, a, e[s + 12], 11, -421815835), r, i, e[s + 15], 16, 530742520), n, r, e[s + 2], 23, -995338651), a = p(a, n = p(n, r = p(r, i, a, n, e[s + 0], 6, -198630844), i, a, e[s + 7], 10, 1126891415), r, i, e[s + 14], 15, -1416354905), n, r, e[s + 5], 21, -57434055), a = p(a, n = p(n, r = p(r, i, a, n, e[s + 12], 6, 1700485571), i, a, e[s + 3], 10, -1894986606), r, i, e[s + 10], 15, -1051523), n, r, e[s + 1], 21, -2054922799), a = p(a, n = p(n, r = p(r, i, a, n, e[s + 8], 6, 1873313359), i, a, e[s + 15], 10, -30611744), r, i, e[s + 6], 15, -1560198380), n, r, e[s + 13], 21, 1309151649), a = p(a, n = p(n, r = p(r, i, a, n, e[s + 4], 6, -145523070), i, a, e[s + 11], 10, -1120210379), r, i, e[s + 2], 15, 718787259), n, r, e[s + 9], 21, -343485551),
                    r = g(r, o),
                    i = g(i, l),
                    a = g(a, u),
                    n = g(n, d)
                }
                return Array(r, i, a, n)
            }(function(e) {
                for (var t = Array(), r = (1 << n) - 1, i = 0; i < e.length * n; i += n)
                    t[i >> 5] |= (e.charCodeAt(i / n) & r) << i % 32;
                return t
            }(t = e), t.length * n))
        };
var oriralSign = "eDu_51Cto_siyuanTlw";
var sign = function (lid) {
    return MD5(lid + oriralSign).toString();
};