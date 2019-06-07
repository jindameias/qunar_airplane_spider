m_js = r'''
	var lib_Hasher_createHelper;
	(function(n, r) {
		lib_Hasher_createHelper = r().lib.Hasher._createHelper();
		console.log(lib_Hasher_createHelper)

	})(this, function() {
		var e = e || function(e, t) {
			var n = Object.create || function() {
				function e() {}

				return function(t) {
					var n;
					e.prototype = t;
					n = new e;
					e.prototype = null;
					return n
				}
			}();
			var r = {};
			var i = r.lib = {};
			var s = i.Base = function() {
				return {
					extend: function(e) {
						var t = n(this);
						if (e) {
							t.mixIn(e)
						}
						if (!t.hasOwnProperty("init") || this.init === t.init) {
							t.init = function() {
								t.$super.init.apply(this, arguments)
							}
						}
						t.init.prototype = t;
						t.$super = this;
						return t
					},
					create: function() {
						var e = this.extend();
						e.init.apply(e, arguments);
						return e
					},
					init: function() {},
					mixIn: function(e) {
						for (var t in e) {
							if (e.hasOwnProperty(t)) {
								this[t] = e[t]
							}
						}
						if (e.hasOwnProperty("toString")) {
							this.toString = e.toString
						}
					},
					clone: function() {
						return this.init.prototype.extend(this)
					}
				}
			}();
			var o = i.WordArray = s.extend({
				init: function(e, n) {
					e = this.words = e || [];
					if (n != t) {
						this.sigBytes = n
					} else {
						this.sigBytes = e.length * 4
					}
				},
				toString: function(e) {
					return (e || a).stringify(this)
				},
				concat: function(e) {
					var t = this.words;
					var n = e.words;
					var r = this.sigBytes;
					var i = e.sigBytes;
					this.clamp();
					if (r % 4) {
						for (var s = 0; s < i; s++) {
							var o = n[s >>> 2] >>> 24 - s % 4 * 8 & 255;
							t[r + s >>> 2] |= o << 24 - (r + s) % 4 * 8
						}
					} else {
						for (var s = 0; s < i; s += 4) {
							t[r + s >>> 2] = n[s >>> 2]
						}
					}
					this.sigBytes += i;
					return this
				},
				clamp: function() {
					var t = this.words;
					var n = this.sigBytes;
					t[n >>> 2] &= 4294967295 << 32 - n % 4 * 8;
					t.length = e.ceil(n / 4)
				},
				clone: function() {
					var e = s.clone.call(this);
					e.words = this.words.slice(0);
					return e
				},
				random: function(t) {
					var n = [];
					var r = function(t) {
						var t = t;
						var n = 987654321;
						var r = 4294967295;
						return function() {
							n = 36969 * (n & 65535) + (n >> 16) & r;
							t = 18e3 * (t & 65535) + (t >> 16) & r;
							var i = (n << 16) + t & r;
							i /= 4294967296;
							i += .5;
							return i * (e.random() > .5 ? 1 : -1)
						}
					};
					for (var i = 0, s; i < t; i += 4) {
						var u = r((s || e.random()) * 4294967296);
						s = u() * 987654071;
						n.push(u() * 4294967296 | 0)
					}
					return new o.init(n, t)
				}
			});
			var u = r.enc = {};
			var a = u.Hex = {
				stringify: function(e) {
					var t = e.words;
					var n = e.sigBytes;
					var r = [];
					for (var i = 0; i < n; i++) {
						var s = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
						r.push((s >>> 4).toString(16));
						r.push((s & 15).toString(16))
					}
					return r.join("")
				},
				parse: function(e) {
					var t = e.length;
					var n = [];
					for (var r = 0; r < t; r += 2) {
						n[r >>> 3] |= parseInt(e.substr(r, 2), 16) << 24 - r % 8 * 4
					}
					return new o.init(n, t / 2)
				}
			};
			var f = u.Latin1 = {
				stringify: function(e) {
					var t = e.words;
					var n = e.sigBytes;
					var r = [];
					for (var i = 0; i < n; i++) {
						var s = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
						r.push(String.fromCharCode(s))
					}
					return r.join("")
				},
				parse: function(e) {
					var t = e.length;
					var n = [];
					for (var r = 0; r < t; r++) {
						n[r >>> 2] |= (e.charCodeAt(r) & 255) << 24 - r % 4 * 8
					}
					return new o.init(n, t)
				}
			};
			var l = u.Utf8 = {
				stringify: function(e) {
					try {
						return decodeURIComponent(escape(f.stringify(e)))
					} catch (t) {
						throw new Error("Malformed UTF-8 data")
					}
				},
				parse: function(e) {
					return f.parse(unescape(encodeURIComponent(e)))
				}
			};
			var c = i.BufferedBlockAlgorithm = s.extend({
				reset: function() {
					this._data = new o.init;
					this._nDataBytes = 0
				},
				_append: function(e) {
					if (typeof e == "string") {
						e = l.parse(e)
					}
					this._data.concat(e);
					this._nDataBytes += e.sigBytes
				},
				_process: function(t) {
					var n = this._data;
					var r = n.words;
					var i = n.sigBytes;
					var s = this.blockSize;
					var u = s * 4;
					var a = i / u;
					if (t) {
						a = e.ceil(a)
					} else {
						a = e.max((a | 0) - this._minBufferSize, 0)
					}
					var f = a * s;
					var l = e.min(f * 4, i);
					if (f) {
						for (var c = 0; c < f; c += s) {
							this._doProcessBlock(r, c)
						}
						var h = r.splice(0, f);
						n.sigBytes -= l
					}
					return new o.init(h, l)
				},
				clone: function() {
					var e = s.clone.call(this);
					e._data = this._data.clone();
					return e
				},
				_minBufferSize: 0
			});
			var h = i.Hasher = c.extend({
				cfg: s.extend(),
				init: function(e) {
					this.cfg = this.cfg.extend(e);
					this.reset()
				},
				reset: function() {
					c.reset.call(this);
					this._doReset()
				},
				update: function(e) {
					this._append(e);
					this._process();
					return this
				},
				finalize: function(e) {
					if (e) {
						this._append(e)
					}
					var t = this._doFinalize();
					return t
				},
				blockSize: 512 / 32,
				_createHelper: function(e) {
					return function(t, n) {


						function reset(n) {
							xxx = {}
							c_reset.call(xxx);
							xxx._doReset = function(n) {
								if (!n) {
									this._hash = new i_init([1732584193, 4023233417, 2562383102, 271733878])
								} else {
									this._hash = new i_init([1732584193, 4023233417, 2562383102, 271733878, 3285377520])
								}
							}
							xxx._doReset(n)
							return xxx
						}

						function c_reset() {
							xxx._data = new o_init;
							xxx._nDataBytes = 0
						}

						function o_init(e, n) {
							e = this.words = e || [];
							if (n != undefined) {
								this.sigBytes = n
							} else {
								this.sigBytes = e.length * 4
							}
						}

						function i_init(e, n) {
							e = this.words = e || [];
							if (n != undefined) {
								this.sigBytes = n
							} else {
								this.sigBytes = e.length * 4
							}
						}




						function super_extend(e) {
							var t = {};
							if (e) {
								t.mixIn(e)
							}
							if (!t.hasOwnProperty("init") || this.init === t.init) {
								t.init = function() {
									t.$super.init.apply(this, arguments)
								}
							}
							t.init.prototype = t;
							return t
						}

						//--------------------------------------------------------------------------------------------------------------------------------------finalize(t)
						function finalize(e, reset, n) {
							if (e) {
								reset._append = function(e) {
									if (typeof e == "string") {
										e = l.parse(e)
									}
									concat = function(e, this_data) {
										var t = this_data.words;
										var n = e.words;
										var r = this_data.sigBytes;
										var i = e.sigBytes;
										clamp = function(this_data) {
											var t = this_data.words;
											var n = this_data.sigBytes;
											t[n >>> 2] &= 4294967295 << 32 - n % 4 * 8;
											t.length = Math.ceil(n / 4)
										}
										clamp(this_data);
										if (r % 4) {
											for (var s = 0; s < i; s++) {
												var o = n[s >>> 2] >>> 24 - s % 4 * 8 & 255;
												t[r + s >>> 2] |= o << 24 - (r + s) % 4 * 8
											}
										} else {
											for (var s = 0; s < i; s += 4) {
												t[r + s >>> 2] = n[s >>> 2]
											}
										}
										this_data.sigBytes += i;
										return this_data
									}

									concat(e, this._data);
									this._nDataBytes += e.sigBytes
								}
								reset._append(e)
							}
							reset._doFinalize = function() {
								var e = this._data;
								var n = e.words;
								var r = this._nDataBytes * 8;
								var i = e.sigBytes * 8;
								n[i >>> 5] |= 128 << 24 - i % 32;
								var s = Math.floor(r / 4294967296);
								var o = r;
								n[(i + 64 >>> 9 << 4) + 15] = (s << 8 | s >>> 24) & 16711935 | (s << 24 | s >>> 8) & 4278255360;
								n[(i + 64 >>> 9 << 4) + 14] = (o << 8 | o >>> 24) & 16711935 | (o << 24 | o >>> 8) & 4278255360;
								e.sigBytes = (n.length + 1) * 4;
								this._process();
								var u = this._hash;
								var a = u.words;
								for (var f = 0; f < 4; f++) {
									var l = a[f];
									a[f] = (l << 8 | l >>> 24) & 16711935 | (l << 24 | l >>> 8) & 4278255360
								}
								return u
							}
							reset._process = function(num, t) {
								"use strict";
								var n = this._data;
								var r = n.words;
								var i = n.sigBytes;
								var s = 16;
								var u = s * 4;
								var a = i / u;

								if (t) {
									a = Math.ceil(a)
								} else {
									a = Math.max((a | 0) - 0, 0)
								}
								var f = a * s;
								var l = Math.min(f * 4, i);
								if (f) {
									for (var c = 0; c < f; c += s) {
										if (!num) {
											this._doProcessBlock(r, c)
										} else {
											this._doProcessBlock2(r, c)
										}
									}
									var h = r.splice(0, f);
									n.sigBytes -= l
								}
								return new o.init(h, l)
							}
							reset._doProcessBlock = function(e, t) {
								for (var n = 0; n < 16; n++) {
									var r = t + n;
									var i = e[r];
									e[r] = (i << 8 | i >>> 24) & 16711935 | (i << 24 | i >>> 8) & 4278255360
								}
								var s = this._hash.words;
								var o = e[t + 0];
								var a = e[t + 1];
								var p = e[t + 2];
								var d = e[t + 3];
								var v = e[t + 4];
								var m = e[t + 5];
								var g = e[t + 6];
								var y = e[t + 7];
								var b = e[t + 8];
								var w = e[t + 9];
								var E = e[t + 10];
								var S = e[t + 11];
								var x = e[t + 12];
								var N = e[t + 13];
								var C = e[t + 14];
								var k = e[t + 15];
								var L = s[0];
								var A = s[1];
								var O = s[2];
								var M = s[3];
								var u = [];
								(function() {
									for (var e = 0; e < 64; e++) {
										u[e] = Math.abs(Math.sin(e + 1)) * 4294967296 | 0
									}
								})();

								function f(e, t, n, r, i, s, o) {
									var u = e + (t & n | ~t & r) + i + o;
									return (u << s | u >>> 32 - s) + t
								}

								function l(e, t, n, r, i, s, o) {
									var u = e + (t & r | n & ~r) + i + o;
									return (u << s | u >>> 32 - s) + t
								}

								function c(e, t, n, r, i, s, o) {
									var u = e + (t ^ n ^ r) + i + o;
									return (u << s | u >>> 32 - s) + t
								}

								function h(e, t, n, r, i, s, o) {
									var u = e + (n ^ (t | ~r)) + i + o;
									return (u << s | u >>> 32 - s) + t
								}
								L = f(L, A, O, M, o, 7, u[0]);
								M = f(M, L, A, O, a, 12, u[1]);
								O = f(O, M, L, A, p, 17, u[2]);
								A = f(A, O, M, L, d, 22, u[3]);
								L = f(L, A, O, M, v, 7, u[4]);
								M = f(M, L, A, O, m, 12, u[5]);
								O = f(O, M, L, A, g, 17, u[6]);
								A = f(A, O, M, L, y, 22, u[7]);
								L = f(L, A, O, M, b, 7, u[8]);
								M = f(M, L, A, O, w, 12, u[9]);
								O = f(O, M, L, A, E, 17, u[10]);
								A = f(A, O, M, L, S, 22, u[11]);
								L = f(L, A, O, M, x, 7, u[12]);
								M = f(M, L, A, O, N, 12, u[13]);
								O = f(O, M, L, A, C, 17, u[14]);
								A = f(A, O, M, L, k, 22, u[15]);
								L = l(L, A, O, M, a, 5, u[16]);
								M = l(M, L, A, O, g, 9, u[17]);
								O = l(O, M, L, A, S, 14, u[18]);
								A = l(A, O, M, L, o, 20, u[19]);
								L = l(L, A, O, M, m, 5, u[20]);
								M = l(M, L, A, O, E, 9, u[21]);
								O = l(O, M, L, A, k, 14, u[22]);
								A = l(A, O, M, L, v, 20, u[23]);
								L = l(L, A, O, M, w, 5, u[24]);
								M = l(M, L, A, O, C, 9, u[25]);
								O = l(O, M, L, A, d, 14, u[26]);
								A = l(A, O, M, L, b, 20, u[27]);
								L = l(L, A, O, M, N, 5, u[28]);
								M = l(M, L, A, O, p, 9, u[29]);
								O = l(O, M, L, A, y, 14, u[30]);
								A = l(A, O, M, L, x, 20, u[31]);
								L = c(L, A, O, M, m, 4, u[32]);
								M = c(M, L, A, O, b, 11, u[33]);
								O = c(O, M, L, A, S, 16, u[34]);
								A = c(A, O, M, L, C, 23, u[35]);
								L = c(L, A, O, M, a, 4, u[36]);
								M = c(M, L, A, O, v, 11, u[37]);
								O = c(O, M, L, A, y, 16, u[38]);
								A = c(A, O, M, L, E, 23, u[39]);
								L = c(L, A, O, M, N, 4, u[40]);
								M = c(M, L, A, O, o, 11, u[41]);
								O = c(O, M, L, A, d, 16, u[42]);
								A = c(A, O, M, L, g, 23, u[43]);
								L = c(L, A, O, M, w, 4, u[44]);
								M = c(M, L, A, O, x, 11, u[45]);
								O = c(O, M, L, A, k, 16, u[46]);
								A = c(A, O, M, L, p, 23, u[47]);
								L = h(L, A, O, M, o, 6, u[48]);
								M = h(M, L, A, O, y, 10, u[49]);
								O = h(O, M, L, A, C, 15, u[50]);
								A = h(A, O, M, L, m, 21, u[51]);
								L = h(L, A, O, M, x, 6, u[52]);
								M = h(M, L, A, O, d, 10, u[53]);
								O = h(O, M, L, A, E, 15, u[54]);
								A = h(A, O, M, L, a, 21, u[55]);
								L = h(L, A, O, M, b, 6, u[56]);
								M = h(M, L, A, O, k, 10, u[57]);
								O = h(O, M, L, A, g, 15, u[58]);
								A = h(A, O, M, L, N, 21, u[59]);
								L = h(L, A, O, M, v, 6, u[60]);
								M = h(M, L, A, O, S, 10, u[61]);
								O = h(O, M, L, A, p, 15, u[62]);
								A = h(A, O, M, L, w, 21, u[63]);
								s[0] = s[0] + L | 0;
								s[1] = s[1] + A | 0;
								s[2] = s[2] + O | 0;
								s[3] = s[3] + M | 0
							}
							reset._doFinalize2 = function(num) {
								var e = this._data;
								var t = e.words;
								var n = this._nDataBytes * 8;
								var r = e.sigBytes * 8;
								t[r >>> 5] |= 128 << 24 - r % 32;
								t[(r + 64 >>> 9 << 4) + 14] = Math.floor(n / 4294967296);
								t[(r + 64 >>> 9 << 4) + 15] = n;
								e.sigBytes = t.length * 4;
								this._process(num);
								return this._hash
							}
							reset._doProcessBlock2 = function(e, t, num) {
								var n = this._hash.words;
								var r = n[0];
								var i = n[1];
								var s = n[2];
								var u = n[3];
								var a = n[4];
								for (var f = 0; f < 80; f++) {
									if (f < 16) {
										o[f] = e[t + f] | 0
									} else {
										var l = o[f - 3] ^ o[f - 8] ^ o[f - 14] ^ o[f - 16];
										o[f] = l << 1 | l >>> 31
									}
									var c = (r << 5 | r >>> 27) + a + o[f];
									if (f < 20) {
										c += (i & s | ~i & u) + 1518500249
									} else if (f < 40) {
										c += (i ^ s ^ u) + 1859775393
									} else if (f < 60) {
										c += (i & s | i & u | s & u) - 1894007588
									} else {
										c += (i ^ s ^ u) - 899497514
									}
									a = u;
									u = s;
									s = i << 30 | i >>> 2;
									i = r;
									r = c
								}
								n[0] = n[0] + r | 0;
								n[1] = n[1] + i | 0;
								n[2] = n[2] + s | 0;
								n[3] = n[3] + u | 0;
								n[4] = n[4] + a | 0
							}
							if (!n) {
								var t = reset._doFinalize();
							} else {
								var t = reset._doFinalize2(n);
							}
							return t
						}

						return finalize(t, reset(n), n)
					}
				},
				_createHmacHelper: function(e) {
					return function(t, n) {
						return (new p.HMAC.init(e, n)).finalize(t)
					}
				}
			});
			var p = r.algo = {};
			return r
		}(Math);
		return e
	})

	//------------------------------------------------------------------------------------------------------------------------------------------------------------------
	//------------------------------------------------------------------------------------------------------------------------------------------------------------------




	t = {
		__esModule: true
	}

	function a(e) {
		return e && e.__esModule ? e : {
			"default": e
		}
	}

	function f(e, t) {
		if (!(e instanceof t)) {
			throw new TypeError("Cannot call a class as a function")
		}
	}
	Object.defineProperty(t, "__esModule", {
		value: true
	});
	var r = function() {
		function e(e, t) {
			for (var n = 0; n < t.length; n++) {
				var r = t[n];
				r.enumerable = r.enumerable || false;
				r.configurable = true;
				if ("value" in r)
					r.writable = true;
				Object.defineProperty(e, r.key, r)
			}
		}
		return function(t, n, r) {
			if (n)
				e(t.prototype, n);
			if (r)
				e(t, r);
			return t
		}
	}();

	var l = function() {
		function e() {
			f(this, e);
			this.qtTime = [83, 80, 56, 56, 58];
			this.cookieToken = [83, 80, 54, 58];
			this.tokenStr = [115, 119, 112, 99, 116, 97, 99, 114, 107, 97, 118, 113, 109, 103, 112]
		}
		r(e, [{
				key: "getQN668",
				value: function(QN668) {
					var n = [
						"QN668=" + QN668
					];
					for (var r = 0; r < n.length; r++) {
						var i = n[r].split("=");

						return decodeURIComponent(i[1])
					}
					return null
				}
			},
			{
				key: "getCookie",
				value: function(t) {
					var n = [
						"Alina=e65b9544-eecf59-33470412-8781e218-74639483999a",
						"QN48=45097701-b96b-4fa2-9b61-6c010392f117",
						"QN668=51%2C55%2C55%2C59%2C55%2C55%2C53%2C54%2C58%2C54%2C52%2C54%2C59"
					];
					for (var r = 0; r < n.length; r++) {
						var i = n[r].split("=");
						if (i[0] === t) {
							return decodeURIComponent(i[1])
						}
					}
					return null
				}
			}, {
				key: "getRandomKey",
				value: function(t) {
					var stringify = function(e) {
						var t = e.words;
						var n = e.sigBytes;
						var r = [];
						for (var i = 0; i < n; i++) {
							var s = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
							r.push((s >>> 4).toString(16));
							r.push((s & 15).toString(16))
						}
						return r.join("")
					}

					function toString(this_encrpy, e) {
						return stringify(this_encrpy)
					}
					var n = "";
					var r = ("" + t).substr(4);
					r.split("").forEach(function(e) {
						n += e.charCodeAt()
					});
					var i = toString((0, l["default"])(n));
					return i.substr(-6)
				}
			}, {
				key: "getToken",
				value: function(QN668, QN48) {
					var t = {};
					t[this.getRandomKey(this.getQtTime(this.getQN668(QN668)))] = this.encrypt(QN668, QN48);
					return t
				}
			}, {
				key: "encryptFunction",
				value: function() {
					var stringify = function(e) {
						var t = e.words;
						var n = e.sigBytes;
						var r = [];
						for (var i = 0; i < n; i++) {
							var s = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
							r.push((s >>> 4).toString(16));
							r.push((s & 15).toString(16))
						}
						return r.join("")
					}

					function toString(this_encrpy, e) {
						return stringify(this_encrpy)
					}
					return [function(e) {
						var t = toString((0, l["default"])(e, 1));
						var res = toString((0, l["default"])(t, ));
						console.log(res)
						return res
					}, function(e) {
						var t = toString((0, l["default"])(e));
						var res = toString((0, l["default"])(t, 1));
						console.log(res)
						return res
					}]
				}
			}, {
				key: "dencryptCode",
				value: function(t) {
					return t.map(function(e) {
						return String.fromCharCode(e - 2)
					}).join("")
				}
			}, {
				key: "getQtTime",
				value: function(t) {
					return t ? Number(t.split(",").map(function(e) {
						return String.fromCharCode(e - 2)
					}).join("")) : 0
				}
			}, {
				key: "getTokenStr",
				value: function(QN48) {
					var t = this.dencryptCode(this.tokenStr);
					var n = null;
					var r = null;
					return decodeURIComponent(QN48)
				}
			}, {
				key: "encrypt",
				value: function(QN668_, QN48) {
					var t = this.getTokenStr(QN48),
						n = this.getQtTime(this.getQN668(QN668_)),
						r = n % 2;
					return this.encryptFunction()[r](t + n)
				}
			}
		]);
		return e
	}();
	t["default"] = new l






	//------------------------------------------------------------------------------------------------------------------------------------------------------------------
	//------------------------------------------------------------------------------------------------------------------------------------------------------------------





	// console.log(t)


	function v(e) {
		return e && e.__esModule ? e : {
			"default": e
		}
	}
	var l = v(lib_Hasher_createHelper);

	var h = v(t)


	var stringify = function(e) {
		var t = e.words;
		var n = e.sigBytes;
		var r = [];
		for (var i = 0; i < n; i++) {
			var s = t[i >>> 2] >>> 24 - i % 4 * 8 & 255;
			r.push((s >>> 4).toString(16));
			r.push((s & 15).toString(16))
		}
		return r.join("")
	}

	function toString(this_encrpy, e) {
		return stringify(this_encrpy)
	}

	function result_m_num(QN668, QN48) {
		var result = toString((0, l["default"])(h["default"].encrypt(QN668, QN48)))
		//console.log('11:', result)
		var headers_ = t["default"].getToken(QN668, QN48)
		//console.log('22:', headers_)
		return [result, headers_]
	}

'''
