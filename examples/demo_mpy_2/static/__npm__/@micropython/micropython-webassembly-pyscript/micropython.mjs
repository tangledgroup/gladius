// node_modules/@micropython/micropython-webassembly-pyscript/micropython.mjs
var _scriptName;
var _createMicroPythonModule = (_scriptName = import.meta.url, async function(moduleArg = {}) {
  var moduleRtn, readyPromiseResolve, readyPromiseReject, Module2 = moduleArg, readyPromise = new Promise((resolve, reject) => {
    readyPromiseResolve = resolve, readyPromiseReject = reject;
  });
  ["_free", "_malloc", "_mp_js_init", "_mp_js_repl_init", "_mp_js_repl_process_char", "_mp_hal_get_interrupt_char", "_mp_sched_keyboard_interrupt", "_mp_js_do_exec", "_mp_js_do_exec_async", "_mp_js_do_import", "_mp_js_register_js_module", "_proxy_c_free_obj", "_proxy_c_init", "_proxy_c_to_js_call", "_proxy_c_to_js_delete_attr", "_proxy_c_to_js_dir", "_proxy_c_to_js_get_array", "_proxy_c_to_js_get_dict", "_proxy_c_to_js_get_iter", "_proxy_c_to_js_get_type", "_proxy_c_to_js_has_attr", "_proxy_c_to_js_iternext", "_proxy_c_to_js_lookup_attr", "_proxy_c_to_js_resume", "_proxy_c_to_js_store_attr", "_proxy_convert_mp_to_js_obj_cside", "_memory", "___indirect_function_table", "_proxy_convert_mp_to_js_then_js_to_mp_obj_jsside", "_proxy_convert_mp_to_js_then_js_to_js_then_js_to_mp_obj_jsside", "_js_get_proxy_js_ref_info", "_has_attr", "_lookup_attr", "_store_attr", "_call0", "_call1", "_call2", "_calln", "_call0_kwarg", "_call1_kwarg", "_js_reflect_construct", "_js_get_iter", "_js_iter_next", "_js_subscr_load", "_js_subscr_store", "_proxy_js_free_obj", "_js_check_existing", "_js_get_error_info", "_js_then_resolve", "_js_then_reject", "_js_then_continue", "_create_promise", "onRuntimeInitialized"].forEach((prop2) => {
    Object.getOwnPropertyDescriptor(readyPromise, prop2) || Object.defineProperty(readyPromise, prop2, { get: () => abort("You are getting " + prop2 + " on the Promise object, instead of the instance. Use .then() to get called back with the instance, see the MODULARIZE docs in src/settings.js"), set: () => abort("You are setting " + prop2 + " on the Promise object, instead of the instance. Use .then() to get called back with the instance, see the MODULARIZE docs in src/settings.js") });
  });
  var ENVIRONMENT_IS_WEB = "object" == typeof window, ENVIRONMENT_IS_WORKER = "function" == typeof importScripts, ENVIRONMENT_IS_NODE = "object" == typeof process && "object" == typeof process.versions && "string" == typeof process.versions.node, ENVIRONMENT_IS_SHELL = !ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_NODE && !ENVIRONMENT_IS_WORKER;
  if (Module2.ENVIRONMENT) throw new Error("Module.ENVIRONMENT has been deprecated. To force the environment, use the ENVIRONMENT compile-time option (for example, -sENVIRONMENT=web or -sENVIRONMENT=node)");
  if (ENVIRONMENT_IS_NODE) {
    const { createRequire } = await import("module");
    var require2 = createRequire(import.meta.url);
  }
  var readAsync, readBinary, moduleOverrides = Object.assign({}, Module2), scriptDirectory = "";
  if (ENVIRONMENT_IS_NODE) {
    if ("undefined" == typeof process || !process.release || "node" !== process.release.name) throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)");
    var nodeVersion = process.versions.node, numericVersion = nodeVersion.split(".").slice(0, 3);
    if ((numericVersion = 1e4 * numericVersion[0] + 100 * numericVersion[1] + 1 * numericVersion[2].split("-")[0]) < 16e4) throw new Error("This emscripten-generated code requires node v16.0.0 (detected v" + nodeVersion + ")");
    var fs = require2("fs"), nodePath = require2("path");
    scriptDirectory = require2("url").fileURLToPath(new URL("./", import.meta.url)), readBinary = (filename) => {
      filename = isFileURI(filename) ? new URL(filename) : nodePath.normalize(filename);
      var ret = fs.readFileSync(filename);
      return assert(ret.buffer), ret;
    }, readAsync = (filename, binary = true) => (filename = isFileURI(filename) ? new URL(filename) : nodePath.normalize(filename), new Promise((resolve, reject) => {
      fs.readFile(filename, binary ? void 0 : "utf8", (err2, data) => {
        err2 ? reject(err2) : resolve(binary ? data.buffer : data);
      });
    })), !Module2.thisProgram && process.argv.length > 1 && process.argv[1].replace(/\\/g, "/"), process.argv.slice(2);
  } else if (ENVIRONMENT_IS_SHELL) {
    if ("object" == typeof process && "function" == typeof require2 || "object" == typeof window || "function" == typeof importScripts) throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)");
  } else {
    if (!ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_WORKER) throw new Error("environment detection error");
    if (ENVIRONMENT_IS_WORKER ? scriptDirectory = self.location.href : "undefined" != typeof document && document.currentScript && (scriptDirectory = document.currentScript.src), _scriptName && (scriptDirectory = _scriptName), scriptDirectory = scriptDirectory.startsWith("blob:") ? "" : scriptDirectory.substr(0, scriptDirectory.replace(/[?#].*/, "").lastIndexOf("/") + 1), "object" != typeof window && "function" != typeof importScripts) throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)");
    ENVIRONMENT_IS_WORKER && (readBinary = (url) => {
      var xhr = new XMLHttpRequest();
      return xhr.open("GET", url, false), xhr.responseType = "arraybuffer", xhr.send(null), new Uint8Array(xhr.response);
    }), readAsync = (url) => isFileURI(url) ? new Promise((resolve, reject) => {
      var xhr = new XMLHttpRequest();
      xhr.open("GET", url, true), xhr.responseType = "arraybuffer", xhr.onload = () => {
        200 == xhr.status || 0 == xhr.status && xhr.response ? resolve(xhr.response) : reject(xhr.status);
      }, xhr.onerror = reject, xhr.send(null);
    }) : fetch(url, { credentials: "same-origin" }).then((response) => response.ok ? response.arrayBuffer() : Promise.reject(new Error(response.status + " : " + response.url)));
  }
  var prop, out = Module2.print || console.log.bind(console), err = Module2.printErr || console.error.bind(console);
  Object.assign(Module2, moduleOverrides), moduleOverrides = null, prop = "fetchSettings", Object.getOwnPropertyDescriptor(Module2, prop) && abort(`\`Module.${prop}\` was supplied but \`${prop}\` not included in INCOMING_MODULE_JS_API`), Module2.arguments && Module2.arguments, legacyModuleProp("arguments", "arguments_"), Module2.thisProgram && Module2.thisProgram, legacyModuleProp("thisProgram", "thisProgram"), assert(void 0 === Module2.memoryInitializerPrefixURL, "Module.memoryInitializerPrefixURL option was removed, use Module.locateFile instead"), assert(void 0 === Module2.pthreadMainPrefixURL, "Module.pthreadMainPrefixURL option was removed, use Module.locateFile instead"), assert(void 0 === Module2.cdInitializerPrefixURL, "Module.cdInitializerPrefixURL option was removed, use Module.locateFile instead"), assert(void 0 === Module2.filePackagePrefixURL, "Module.filePackagePrefixURL option was removed, use Module.locateFile instead"), assert(void 0 === Module2.read, "Module.read option was removed"), assert(void 0 === Module2.readAsync, "Module.readAsync option was removed (modify readAsync in JS)"), assert(void 0 === Module2.readBinary, "Module.readBinary option was removed (modify readBinary in JS)"), assert(void 0 === Module2.setWindowTitle, "Module.setWindowTitle option was removed (modify emscripten_set_window_title in JS)"), assert(void 0 === Module2.TOTAL_MEMORY, "Module.TOTAL_MEMORY has been renamed Module.INITIAL_MEMORY"), legacyModuleProp("asm", "wasmExports"), legacyModuleProp("readAsync", "readAsync"), legacyModuleProp("readBinary", "readBinary"), legacyModuleProp("setWindowTitle", "setWindowTitle"), assert(!ENVIRONMENT_IS_SHELL, "shell environment detected but not enabled at build time.  Add `shell` to `-sENVIRONMENT` to enable.");
  var wasmMemory, wasmBinary = Module2.wasmBinary;
  legacyModuleProp("wasmBinary", "wasmBinary"), "object" != typeof WebAssembly && err("no native wasm support detected");
  var HEAP8, HEAPU8, HEAP16, HEAP32, HEAPU32, HEAPF32, HEAPF64, ABORT = false;
  function assert(condition, text) {
    condition || abort("Assertion failed" + (text ? ": " + text : ""));
  }
  function updateMemoryViews() {
    var b = wasmMemory.buffer;
    Module2.HEAP8 = HEAP8 = new Int8Array(b), Module2.HEAP16 = HEAP16 = new Int16Array(b), Module2.HEAPU8 = HEAPU8 = new Uint8Array(b), Module2.HEAPU16 = new Uint16Array(b), Module2.HEAP32 = HEAP32 = new Int32Array(b), Module2.HEAPU32 = HEAPU32 = new Uint32Array(b), Module2.HEAPF32 = HEAPF32 = new Float32Array(b), Module2.HEAPF64 = HEAPF64 = new Float64Array(b);
  }
  function checkStackCookie() {
    if (!ABORT) {
      var max = _emscripten_stack_get_end();
      0 == max && (max += 4);
      var cookie1 = HEAPU32[max >> 2], cookie2 = HEAPU32[max + 4 >> 2];
      34821223 == cookie1 && 2310721022 == cookie2 || abort(`Stack overflow! Stack cookie has been overwritten at ${ptrToString(max)}, expected hex dwords 0x89BACDFE and 0x2135467, but received ${ptrToString(cookie2)} ${ptrToString(cookie1)}`), 1668509029 != HEAPU32[0] && abort("Runtime error: The application has corrupted its heap memory area (address zero)!");
    }
  }
  assert(!Module2.STACK_SIZE, "STACK_SIZE can no longer be set at runtime.  Use -sSTACK_SIZE at link time"), assert("undefined" != typeof Int32Array && "undefined" != typeof Float64Array && null != Int32Array.prototype.subarray && null != Int32Array.prototype.set, "JS engine does not provide full typed array support"), assert(!Module2.wasmMemory, "Use of `wasmMemory` detected.  Use -sIMPORTED_MEMORY to define wasmMemory externally"), assert(!Module2.INITIAL_MEMORY, "Detected runtime INITIAL_MEMORY setting.  Use -sIMPORTED_MEMORY to define wasmMemory dynamically");
  var __ATPRERUN__ = [], __ATINIT__ = [], __ATPOSTRUN__ = [], runtimeInitialized = false;
  assert(Math.imul, "This browser does not support Math.imul(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill"), assert(Math.fround, "This browser does not support Math.fround(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill"), assert(Math.clz32, "This browser does not support Math.clz32(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill"), assert(Math.trunc, "This browser does not support Math.trunc(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill");
  var runDependencies = 0, runDependencyWatcher = null, dependenciesFulfilled = null, runDependencyTracking = {};
  function getUniqueRunDependency(id) {
    for (var orig = id; ; ) {
      if (!runDependencyTracking[id]) return id;
      id = orig + Math.random();
    }
  }
  function addRunDependency(id) {
    runDependencies++, Module2.monitorRunDependencies?.(runDependencies), id ? (assert(!runDependencyTracking[id]), runDependencyTracking[id] = 1, null === runDependencyWatcher && "undefined" != typeof setInterval && (runDependencyWatcher = setInterval(() => {
      if (ABORT) return clearInterval(runDependencyWatcher), void (runDependencyWatcher = null);
      var shown = false;
      for (var dep in runDependencyTracking) shown || (shown = true, err("still waiting on run dependencies:")), err(`dependency: ${dep}`);
      shown && err("(end of list)");
    }, 1e4))) : err("warning: run dependency added without ID");
  }
  function removeRunDependency(id) {
    if (runDependencies--, Module2.monitorRunDependencies?.(runDependencies), id ? (assert(runDependencyTracking[id]), delete runDependencyTracking[id]) : err("warning: run dependency removed without ID"), 0 == runDependencies && (null !== runDependencyWatcher && (clearInterval(runDependencyWatcher), runDependencyWatcher = null), dependenciesFulfilled)) {
      var callback = dependenciesFulfilled;
      dependenciesFulfilled = null, callback();
    }
  }
  function abort(what) {
    Module2.onAbort?.(what), err(what = "Aborted(" + what + ")"), ABORT = true;
    var e = new WebAssembly.RuntimeError(what);
    throw readyPromiseReject(e), e;
  }
  var wasmBinaryFile, tempDouble, tempI64, isDataURI = (filename) => filename.startsWith("data:application/octet-stream;base64,"), isFileURI = (filename) => filename.startsWith("file://");
  function createExportWrapper(name, nargs) {
    return (...args) => {
      assert(runtimeInitialized, `native function \`${name}\` called before runtime initialization`);
      var f = wasmExports[name];
      return assert(f, `exported native function \`${name}\` not found`), assert(args.length <= nargs, `native function \`${name}\` called with ${args.length} args but expects ${nargs}`), f(...args);
    };
  }
  function findWasmBinary() {
    if (Module2.locateFile) {
      var f = "micropython.wasm";
      return isDataURI(f) ? f : (path = f, Module2.locateFile ? Module2.locateFile(path, scriptDirectory) : scriptDirectory + path);
    }
    var path;
    return new URL("micropython.wasm", import.meta.url).href;
  }
  function getBinarySync(file) {
    if (file == wasmBinaryFile && wasmBinary) return new Uint8Array(wasmBinary);
    if (readBinary) return readBinary(file);
    throw "both async and sync fetching of the wasm failed";
  }
  function instantiateArrayBuffer(binaryFile, imports, receiver) {
    return function(binaryFile2) {
      return wasmBinary ? Promise.resolve().then(() => getBinarySync(binaryFile2)) : readAsync(binaryFile2).then((response) => new Uint8Array(response), () => getBinarySync(binaryFile2));
    }(binaryFile).then((binary) => WebAssembly.instantiate(binary, imports)).then(receiver, (reason) => {
      err(`failed to asynchronously prepare wasm: ${reason}`), isFileURI(wasmBinaryFile) && err(`warning: Loading from a file URI (${wasmBinaryFile}) is not supported in most browsers. See https://emscripten.org/docs/getting_started/FAQ.html#how-do-i-run-a-local-webserver-for-testing-why-does-my-program-stall-in-downloading-or-preparing`), abort(reason);
    });
  }
  function legacyModuleProp(prop2, newName, incoming = true) {
    Object.getOwnPropertyDescriptor(Module2, prop2) || Object.defineProperty(Module2, prop2, { configurable: true, get() {
      abort(`\`Module.${prop2}\` has been replaced by \`${newName}\`` + (incoming ? " (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)" : ""));
    } });
  }
  function isExportedByForceFilesystem(name) {
    return "FS_createPath" === name || "FS_createDataFile" === name || "FS_createPreloadedFile" === name || "FS_unlink" === name || "addRunDependency" === name || "FS_createLazyFile" === name || "FS_createDevice" === name || "removeRunDependency" === name;
  }
  function missingGlobal(sym, msg) {
    "undefined" != typeof globalThis && Object.defineProperty(globalThis, sym, { configurable: true, get() {
      warnOnce(`\`${sym}\` is not longer defined by emscripten. ${msg}`);
    } });
  }
  function unexportedRuntimeSymbol(sym) {
    Object.getOwnPropertyDescriptor(Module2, sym) || Object.defineProperty(Module2, sym, { configurable: true, get() {
      var msg = `'${sym}' was not exported. add it to EXPORTED_RUNTIME_METHODS (see the Emscripten FAQ)`;
      isExportedByForceFilesystem(sym) && (msg += ". Alternatively, forcing filesystem support (-sFORCE_FILESYSTEM) can export this for you"), abort(msg);
    } });
  }
  (() => {
    var h16 = new Int16Array(1), h8 = new Int8Array(h16.buffer);
    if (h16[0] = 25459, 115 !== h8[0] || 99 !== h8[1]) throw "Runtime error: expected the system to be little-endian! (Run with -sSUPPORT_BIG_ENDIAN to bypass)";
  })(), missingGlobal("buffer", "Please use HEAP8.buffer or wasmMemory.buffer"), missingGlobal("asm", "Please use wasmExports instead");
  var callRuntimeCallbacks = (callbacks) => {
    for (; callbacks.length > 0; ) callbacks.shift()(Module2);
  };
  function getValue(ptr, type = "i8") {
    switch (type.endsWith("*") && (type = "*"), type) {
      case "i1":
      case "i8":
        return HEAP8[ptr];
      case "i16":
        return HEAP16[ptr >> 1];
      case "i32":
        return HEAP32[ptr >> 2];
      case "i64":
        abort("to do getValue(i64) use WASM_BIGINT");
      case "float":
        return HEAPF32[ptr >> 2];
      case "double":
        return HEAPF64[ptr >> 3];
      case "*":
        return HEAPU32[ptr >> 2];
      default:
        abort(`invalid type for getValue: ${type}`);
    }
  }
  Module2.noExitRuntime;
  var ptrToString = (ptr) => (assert("number" == typeof ptr), "0x" + (ptr >>>= 0).toString(16).padStart(8, "0")), stackRestore = (val) => __emscripten_stack_restore(val), stackSave = () => _emscripten_stack_get_current(), warnOnce = (text) => {
    warnOnce.shown ||= {}, warnOnce.shown[text] || (warnOnce.shown[text] = 1, ENVIRONMENT_IS_NODE && (text = "warning: " + text), err(text));
  }, PATH = { isAbs: (path) => "/" === path.charAt(0), splitPath: (filename) => /^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/.exec(filename).slice(1), normalizeArray: (parts, allowAboveRoot) => {
    for (var up = 0, i = parts.length - 1; i >= 0; i--) {
      var last = parts[i];
      "." === last ? parts.splice(i, 1) : ".." === last ? (parts.splice(i, 1), up++) : up && (parts.splice(i, 1), up--);
    }
    if (allowAboveRoot) for (; up; up--) parts.unshift("..");
    return parts;
  }, normalize: (path) => {
    var isAbsolute = PATH.isAbs(path), trailingSlash = "/" === path.substr(-1);
    return (path = PATH.normalizeArray(path.split("/").filter((p) => !!p), !isAbsolute).join("/")) || isAbsolute || (path = "."), path && trailingSlash && (path += "/"), (isAbsolute ? "/" : "") + path;
  }, dirname: (path) => {
    var result = PATH.splitPath(path), root = result[0], dir = result[1];
    return root || dir ? (dir && (dir = dir.substr(0, dir.length - 1)), root + dir) : ".";
  }, basename: (path) => {
    if ("/" === path) return "/";
    var lastSlash = (path = (path = PATH.normalize(path)).replace(/\/$/, "")).lastIndexOf("/");
    return -1 === lastSlash ? path : path.substr(lastSlash + 1);
  }, join: (...paths) => PATH.normalize(paths.join("/")), join2: (l, r) => PATH.normalize(l + "/" + r) }, randomFill = (view) => (randomFill = (() => {
    if ("object" == typeof crypto && "function" == typeof crypto.getRandomValues) return (view2) => crypto.getRandomValues(view2);
    if (ENVIRONMENT_IS_NODE) try {
      var crypto_module = require2("crypto");
      if (crypto_module.randomFillSync) return (view2) => crypto_module.randomFillSync(view2);
      var randomBytes = crypto_module.randomBytes;
      return (view2) => (view2.set(randomBytes(view2.byteLength)), view2);
    } catch (e) {
    }
    abort("no cryptographic support found for randomDevice. consider polyfilling it if you want to use something insecure like Math.random(), e.g. put this in a --pre-js: var crypto = { getRandomValues: (array) => { for (var i = 0; i < array.length; i++) array[i] = (Math.random()*256)|0 } };");
  })())(view), PATH_FS = { resolve: (...args) => {
    for (var resolvedPath = "", resolvedAbsolute = false, i = args.length - 1; i >= -1 && !resolvedAbsolute; i--) {
      var path = i >= 0 ? args[i] : FS.cwd();
      if ("string" != typeof path) throw new TypeError("Arguments to path.resolve must be strings");
      if (!path) return "";
      resolvedPath = path + "/" + resolvedPath, resolvedAbsolute = PATH.isAbs(path);
    }
    return (resolvedAbsolute ? "/" : "") + (resolvedPath = PATH.normalizeArray(resolvedPath.split("/").filter((p) => !!p), !resolvedAbsolute).join("/")) || ".";
  }, relative: (from, to) => {
    function trim(arr) {
      for (var start = 0; start < arr.length && "" === arr[start]; start++) ;
      for (var end = arr.length - 1; end >= 0 && "" === arr[end]; end--) ;
      return start > end ? [] : arr.slice(start, end - start + 1);
    }
    from = PATH_FS.resolve(from).substr(1), to = PATH_FS.resolve(to).substr(1);
    for (var fromParts = trim(from.split("/")), toParts = trim(to.split("/")), length = Math.min(fromParts.length, toParts.length), samePartsLength = length, i = 0; i < length; i++) if (fromParts[i] !== toParts[i]) {
      samePartsLength = i;
      break;
    }
    var outputParts = [];
    for (i = samePartsLength; i < fromParts.length; i++) outputParts.push("..");
    return (outputParts = outputParts.concat(toParts.slice(samePartsLength))).join("/");
  } }, UTF8Decoder = "undefined" != typeof TextDecoder ? new TextDecoder() : void 0, UTF8ArrayToString = (heapOrArray, idx, maxBytesToRead) => {
    for (var endIdx = idx + maxBytesToRead, endPtr = idx; heapOrArray[endPtr] && !(endPtr >= endIdx); ) ++endPtr;
    if (endPtr - idx > 16 && heapOrArray.buffer && UTF8Decoder) return UTF8Decoder.decode(heapOrArray.subarray(idx, endPtr));
    for (var str = ""; idx < endPtr; ) {
      var u0 = heapOrArray[idx++];
      if (128 & u0) {
        var u1 = 63 & heapOrArray[idx++];
        if (192 != (224 & u0)) {
          var u2 = 63 & heapOrArray[idx++];
          if (224 == (240 & u0) ? u0 = (15 & u0) << 12 | u1 << 6 | u2 : (240 != (248 & u0) && warnOnce("Invalid UTF-8 leading byte " + ptrToString(u0) + " encountered when deserializing a UTF-8 string in wasm memory to a JS string!"), u0 = (7 & u0) << 18 | u1 << 12 | u2 << 6 | 63 & heapOrArray[idx++]), u0 < 65536) str += String.fromCharCode(u0);
          else {
            var ch = u0 - 65536;
            str += String.fromCharCode(55296 | ch >> 10, 56320 | 1023 & ch);
          }
        } else str += String.fromCharCode((31 & u0) << 6 | u1);
      } else str += String.fromCharCode(u0);
    }
    return str;
  }, FS_stdin_getChar_buffer = [], lengthBytesUTF8 = (str) => {
    for (var len = 0, i = 0; i < str.length; ++i) {
      var c = str.charCodeAt(i);
      c <= 127 ? len++ : c <= 2047 ? len += 2 : c >= 55296 && c <= 57343 ? (len += 4, ++i) : len += 3;
    }
    return len;
  }, stringToUTF8Array = (str, heap, outIdx, maxBytesToWrite) => {
    if (assert("string" == typeof str, `stringToUTF8Array expects a string (got ${typeof str})`), !(maxBytesToWrite > 0)) return 0;
    for (var startIdx = outIdx, endIdx = outIdx + maxBytesToWrite - 1, i = 0; i < str.length; ++i) {
      var u = str.charCodeAt(i);
      if (u >= 55296 && u <= 57343 && (u = 65536 + ((1023 & u) << 10) | 1023 & str.charCodeAt(++i)), u <= 127) {
        if (outIdx >= endIdx) break;
        heap[outIdx++] = u;
      } else if (u <= 2047) {
        if (outIdx + 1 >= endIdx) break;
        heap[outIdx++] = 192 | u >> 6, heap[outIdx++] = 128 | 63 & u;
      } else if (u <= 65535) {
        if (outIdx + 2 >= endIdx) break;
        heap[outIdx++] = 224 | u >> 12, heap[outIdx++] = 128 | u >> 6 & 63, heap[outIdx++] = 128 | 63 & u;
      } else {
        if (outIdx + 3 >= endIdx) break;
        u > 1114111 && warnOnce("Invalid Unicode code point " + ptrToString(u) + " encountered when serializing a JS string to a UTF-8 string in wasm memory! (Valid unicode code points should be in range 0-0x10FFFF)."), heap[outIdx++] = 240 | u >> 18, heap[outIdx++] = 128 | u >> 12 & 63, heap[outIdx++] = 128 | u >> 6 & 63, heap[outIdx++] = 128 | 63 & u;
      }
    }
    return heap[outIdx] = 0, outIdx - startIdx;
  };
  function intArrayFromString(stringy, dontAddNull, length) {
    var len = length > 0 ? length : lengthBytesUTF8(stringy) + 1, u8array = new Array(len), numBytesWritten = stringToUTF8Array(stringy, u8array, 0, u8array.length);
    return dontAddNull && (u8array.length = numBytesWritten), u8array;
  }
  var wasmTable, TTY = { ttys: [], init() {
  }, shutdown() {
  }, register(dev, ops) {
    TTY.ttys[dev] = { input: [], output: [], ops }, FS.registerDevice(dev, TTY.stream_ops);
  }, stream_ops: { open(stream) {
    var tty = TTY.ttys[stream.node.rdev];
    if (!tty) throw new FS.ErrnoError(43);
    stream.tty = tty, stream.seekable = false;
  }, close(stream) {
    stream.tty.ops.fsync(stream.tty);
  }, fsync(stream) {
    stream.tty.ops.fsync(stream.tty);
  }, read(stream, buffer, offset, length, pos) {
    if (!stream.tty || !stream.tty.ops.get_char) throw new FS.ErrnoError(60);
    for (var bytesRead = 0, i = 0; i < length; i++) {
      var result;
      try {
        result = stream.tty.ops.get_char(stream.tty);
      } catch (e) {
        throw new FS.ErrnoError(29);
      }
      if (void 0 === result && 0 === bytesRead) throw new FS.ErrnoError(6);
      if (null == result) break;
      bytesRead++, buffer[offset + i] = result;
    }
    return bytesRead && (stream.node.timestamp = Date.now()), bytesRead;
  }, write(stream, buffer, offset, length, pos) {
    if (!stream.tty || !stream.tty.ops.put_char) throw new FS.ErrnoError(60);
    try {
      for (var i = 0; i < length; i++) stream.tty.ops.put_char(stream.tty, buffer[offset + i]);
    } catch (e) {
      throw new FS.ErrnoError(29);
    }
    return length && (stream.node.timestamp = Date.now()), i;
  } }, default_tty_ops: { get_char: (tty) => (() => {
    if (!FS_stdin_getChar_buffer.length) {
      var result = null;
      if (ENVIRONMENT_IS_NODE) {
        var buf = Buffer.alloc(256), bytesRead = 0, fd = process.stdin.fd;
        try {
          bytesRead = fs.readSync(fd, buf, 0, 256);
        } catch (e) {
          if (!e.toString().includes("EOF")) throw e;
          bytesRead = 0;
        }
        bytesRead > 0 && (result = buf.slice(0, bytesRead).toString("utf-8"));
      } else "undefined" != typeof window && "function" == typeof window.prompt && null !== (result = window.prompt("Input: ")) && (result += "\n");
      if (!result) return null;
      FS_stdin_getChar_buffer = intArrayFromString(result, true);
    }
    return FS_stdin_getChar_buffer.shift();
  })(), put_char(tty, val) {
    null === val || 10 === val ? (out(UTF8ArrayToString(tty.output, 0)), tty.output = []) : 0 != val && tty.output.push(val);
  }, fsync(tty) {
    tty.output && tty.output.length > 0 && (out(UTF8ArrayToString(tty.output, 0)), tty.output = []);
  }, ioctl_tcgets: (tty) => ({ c_iflag: 25856, c_oflag: 5, c_cflag: 191, c_lflag: 35387, c_cc: [3, 28, 127, 21, 4, 0, 1, 0, 17, 19, 26, 0, 18, 15, 23, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }), ioctl_tcsets: (tty, optional_actions, data) => 0, ioctl_tiocgwinsz: (tty) => [24, 80] }, default_tty1_ops: { put_char(tty, val) {
    null === val || 10 === val ? (err(UTF8ArrayToString(tty.output, 0)), tty.output = []) : 0 != val && tty.output.push(val);
  }, fsync(tty) {
    tty.output && tty.output.length > 0 && (err(UTF8ArrayToString(tty.output, 0)), tty.output = []);
  } } }, mmapAlloc = (size) => {
    abort("internal error: mmapAlloc called but `emscripten_builtin_memalign` native symbol not exported");
  }, MEMFS = { ops_table: null, mount: (mount) => MEMFS.createNode(null, "/", 16895, 0), createNode(parent, name, mode, dev) {
    if (FS.isBlkdev(mode) || FS.isFIFO(mode)) throw new FS.ErrnoError(63);
    MEMFS.ops_table ||= { dir: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr, lookup: MEMFS.node_ops.lookup, mknod: MEMFS.node_ops.mknod, rename: MEMFS.node_ops.rename, unlink: MEMFS.node_ops.unlink, rmdir: MEMFS.node_ops.rmdir, readdir: MEMFS.node_ops.readdir, symlink: MEMFS.node_ops.symlink }, stream: { llseek: MEMFS.stream_ops.llseek } }, file: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr }, stream: { llseek: MEMFS.stream_ops.llseek, read: MEMFS.stream_ops.read, write: MEMFS.stream_ops.write, allocate: MEMFS.stream_ops.allocate, mmap: MEMFS.stream_ops.mmap, msync: MEMFS.stream_ops.msync } }, link: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr, readlink: MEMFS.node_ops.readlink }, stream: {} }, chrdev: { node: { getattr: MEMFS.node_ops.getattr, setattr: MEMFS.node_ops.setattr }, stream: FS.chrdev_stream_ops } };
    var node = FS.createNode(parent, name, mode, dev);
    return FS.isDir(node.mode) ? (node.node_ops = MEMFS.ops_table.dir.node, node.stream_ops = MEMFS.ops_table.dir.stream, node.contents = {}) : FS.isFile(node.mode) ? (node.node_ops = MEMFS.ops_table.file.node, node.stream_ops = MEMFS.ops_table.file.stream, node.usedBytes = 0, node.contents = null) : FS.isLink(node.mode) ? (node.node_ops = MEMFS.ops_table.link.node, node.stream_ops = MEMFS.ops_table.link.stream) : FS.isChrdev(node.mode) && (node.node_ops = MEMFS.ops_table.chrdev.node, node.stream_ops = MEMFS.ops_table.chrdev.stream), node.timestamp = Date.now(), parent && (parent.contents[name] = node, parent.timestamp = node.timestamp), node;
  }, getFileDataAsTypedArray: (node) => node.contents ? node.contents.subarray ? node.contents.subarray(0, node.usedBytes) : new Uint8Array(node.contents) : new Uint8Array(0), expandFileStorage(node, newCapacity) {
    var prevCapacity = node.contents ? node.contents.length : 0;
    if (!(prevCapacity >= newCapacity)) {
      newCapacity = Math.max(newCapacity, prevCapacity * (prevCapacity < 1048576 ? 2 : 1.125) >>> 0), 0 != prevCapacity && (newCapacity = Math.max(newCapacity, 256));
      var oldContents = node.contents;
      node.contents = new Uint8Array(newCapacity), node.usedBytes > 0 && node.contents.set(oldContents.subarray(0, node.usedBytes), 0);
    }
  }, resizeFileStorage(node, newSize) {
    if (node.usedBytes != newSize) if (0 == newSize) node.contents = null, node.usedBytes = 0;
    else {
      var oldContents = node.contents;
      node.contents = new Uint8Array(newSize), oldContents && node.contents.set(oldContents.subarray(0, Math.min(newSize, node.usedBytes))), node.usedBytes = newSize;
    }
  }, node_ops: { getattr(node) {
    var attr = {};
    return attr.dev = FS.isChrdev(node.mode) ? node.id : 1, attr.ino = node.id, attr.mode = node.mode, attr.nlink = 1, attr.uid = 0, attr.gid = 0, attr.rdev = node.rdev, FS.isDir(node.mode) ? attr.size = 4096 : FS.isFile(node.mode) ? attr.size = node.usedBytes : FS.isLink(node.mode) ? attr.size = node.link.length : attr.size = 0, attr.atime = new Date(node.timestamp), attr.mtime = new Date(node.timestamp), attr.ctime = new Date(node.timestamp), attr.blksize = 4096, attr.blocks = Math.ceil(attr.size / attr.blksize), attr;
  }, setattr(node, attr) {
    void 0 !== attr.mode && (node.mode = attr.mode), void 0 !== attr.timestamp && (node.timestamp = attr.timestamp), void 0 !== attr.size && MEMFS.resizeFileStorage(node, attr.size);
  }, lookup(parent, name) {
    throw FS.genericErrors[44];
  }, mknod: (parent, name, mode, dev) => MEMFS.createNode(parent, name, mode, dev), rename(old_node, new_dir, new_name) {
    if (FS.isDir(old_node.mode)) {
      var new_node;
      try {
        new_node = FS.lookupNode(new_dir, new_name);
      } catch (e) {
      }
      if (new_node) for (var i in new_node.contents) throw new FS.ErrnoError(55);
    }
    delete old_node.parent.contents[old_node.name], old_node.parent.timestamp = Date.now(), old_node.name = new_name, new_dir.contents[new_name] = old_node, new_dir.timestamp = old_node.parent.timestamp;
  }, unlink(parent, name) {
    delete parent.contents[name], parent.timestamp = Date.now();
  }, rmdir(parent, name) {
    var node = FS.lookupNode(parent, name);
    for (var i in node.contents) throw new FS.ErrnoError(55);
    delete parent.contents[name], parent.timestamp = Date.now();
  }, readdir(node) {
    var entries = [".", ".."];
    for (var key of Object.keys(node.contents)) entries.push(key);
    return entries;
  }, symlink(parent, newname, oldpath) {
    var node = MEMFS.createNode(parent, newname, 41471, 0);
    return node.link = oldpath, node;
  }, readlink(node) {
    if (!FS.isLink(node.mode)) throw new FS.ErrnoError(28);
    return node.link;
  } }, stream_ops: { read(stream, buffer, offset, length, position) {
    var contents = stream.node.contents;
    if (position >= stream.node.usedBytes) return 0;
    var size = Math.min(stream.node.usedBytes - position, length);
    if (assert(size >= 0), size > 8 && contents.subarray) buffer.set(contents.subarray(position, position + size), offset);
    else for (var i = 0; i < size; i++) buffer[offset + i] = contents[position + i];
    return size;
  }, write(stream, buffer, offset, length, position, canOwn) {
    if (assert(!(buffer instanceof ArrayBuffer)), buffer.buffer === HEAP8.buffer && (canOwn = false), !length) return 0;
    var node = stream.node;
    if (node.timestamp = Date.now(), buffer.subarray && (!node.contents || node.contents.subarray)) {
      if (canOwn) return assert(0 === position, "canOwn must imply no weird position inside the file"), node.contents = buffer.subarray(offset, offset + length), node.usedBytes = length, length;
      if (0 === node.usedBytes && 0 === position) return node.contents = buffer.slice(offset, offset + length), node.usedBytes = length, length;
      if (position + length <= node.usedBytes) return node.contents.set(buffer.subarray(offset, offset + length), position), length;
    }
    if (MEMFS.expandFileStorage(node, position + length), node.contents.subarray && buffer.subarray) node.contents.set(buffer.subarray(offset, offset + length), position);
    else for (var i = 0; i < length; i++) node.contents[position + i] = buffer[offset + i];
    return node.usedBytes = Math.max(node.usedBytes, position + length), length;
  }, llseek(stream, offset, whence) {
    var position = offset;
    if (1 === whence ? position += stream.position : 2 === whence && FS.isFile(stream.node.mode) && (position += stream.node.usedBytes), position < 0) throw new FS.ErrnoError(28);
    return position;
  }, allocate(stream, offset, length) {
    MEMFS.expandFileStorage(stream.node, offset + length), stream.node.usedBytes = Math.max(stream.node.usedBytes, offset + length);
  }, mmap(stream, length, position, prot, flags) {
    if (!FS.isFile(stream.node.mode)) throw new FS.ErrnoError(43);
    var ptr, allocated, contents = stream.node.contents;
    if (2 & flags || !contents || contents.buffer !== HEAP8.buffer) {
      if (allocated = true, !(ptr = mmapAlloc())) throw new FS.ErrnoError(48);
      contents && ((position > 0 || position + length < contents.length) && (contents = contents.subarray ? contents.subarray(position, position + length) : Array.prototype.slice.call(contents, position, position + length)), HEAP8.set(contents, ptr));
    } else allocated = false, ptr = contents.byteOffset;
    return { ptr, allocated };
  }, msync: (stream, buffer, offset, length, mmapFlags) => (MEMFS.stream_ops.write(stream, buffer, 0, length, offset, false), 0) } }, preloadPlugins = Module2.preloadPlugins || [], FS_getMode = (canRead, canWrite) => {
    var mode = 0;
    return canRead && (mode |= 365), canWrite && (mode |= 146), mode;
  }, UTF8ToString = (ptr, maxBytesToRead) => (assert("number" == typeof ptr, `UTF8ToString expects a number (got ${typeof ptr})`), ptr ? UTF8ArrayToString(HEAPU8, ptr, maxBytesToRead) : ""), ERRNO_CODES = { EPERM: 63, ENOENT: 44, ESRCH: 71, EINTR: 27, EIO: 29, ENXIO: 60, E2BIG: 1, ENOEXEC: 45, EBADF: 8, ECHILD: 12, EAGAIN: 6, EWOULDBLOCK: 6, ENOMEM: 48, EACCES: 2, EFAULT: 21, ENOTBLK: 105, EBUSY: 10, EEXIST: 20, EXDEV: 75, ENODEV: 43, ENOTDIR: 54, EISDIR: 31, EINVAL: 28, ENFILE: 41, EMFILE: 33, ENOTTY: 59, ETXTBSY: 74, EFBIG: 22, ENOSPC: 51, ESPIPE: 70, EROFS: 69, EMLINK: 34, EPIPE: 64, EDOM: 18, ERANGE: 68, ENOMSG: 49, EIDRM: 24, ECHRNG: 106, EL2NSYNC: 156, EL3HLT: 107, EL3RST: 108, ELNRNG: 109, EUNATCH: 110, ENOCSI: 111, EL2HLT: 112, EDEADLK: 16, ENOLCK: 46, EBADE: 113, EBADR: 114, EXFULL: 115, ENOANO: 104, EBADRQC: 103, EBADSLT: 102, EDEADLOCK: 16, EBFONT: 101, ENOSTR: 100, ENODATA: 116, ETIME: 117, ENOSR: 118, ENONET: 119, ENOPKG: 120, EREMOTE: 121, ENOLINK: 47, EADV: 122, ESRMNT: 123, ECOMM: 124, EPROTO: 65, EMULTIHOP: 36, EDOTDOT: 125, EBADMSG: 9, ENOTUNIQ: 126, EBADFD: 127, EREMCHG: 128, ELIBACC: 129, ELIBBAD: 130, ELIBSCN: 131, ELIBMAX: 132, ELIBEXEC: 133, ENOSYS: 52, ENOTEMPTY: 55, ENAMETOOLONG: 37, ELOOP: 32, EOPNOTSUPP: 138, EPFNOSUPPORT: 139, ECONNRESET: 15, ENOBUFS: 42, EAFNOSUPPORT: 5, EPROTOTYPE: 67, ENOTSOCK: 57, ENOPROTOOPT: 50, ESHUTDOWN: 140, ECONNREFUSED: 14, EADDRINUSE: 3, ECONNABORTED: 13, ENETUNREACH: 40, ENETDOWN: 38, ETIMEDOUT: 73, EHOSTDOWN: 142, EHOSTUNREACH: 23, EINPROGRESS: 26, EALREADY: 7, EDESTADDRREQ: 17, EMSGSIZE: 35, EPROTONOSUPPORT: 66, ESOCKTNOSUPPORT: 137, EADDRNOTAVAIL: 4, ENETRESET: 39, EISCONN: 30, ENOTCONN: 53, ETOOMANYREFS: 141, EUSERS: 136, EDQUOT: 19, ESTALE: 72, ENOTSUP: 138, ENOMEDIUM: 148, EILSEQ: 25, EOVERFLOW: 61, ECANCELED: 11, ENOTRECOVERABLE: 56, EOWNERDEAD: 62, ESTRPIPE: 135 }, FS = { root: null, mounts: [], devices: {}, streams: [], nextInode: 1, nameTable: null, currentPath: "/", initialized: false, ignorePermissions: true, ErrnoError: class extends Error {
    constructor(errno) {
      for (var key in super(runtimeInitialized ? ((errno2) => UTF8ToString(_strerror(errno2)))(errno) : ""), this.name = "ErrnoError", this.errno = errno, ERRNO_CODES) if (ERRNO_CODES[key] === errno) {
        this.code = key;
        break;
      }
    }
  }, genericErrors: {}, filesystems: null, syncFSRequests: 0, FSStream: class {
    constructor() {
      this.shared = {};
    }
    get object() {
      return this.node;
    }
    set object(val) {
      this.node = val;
    }
    get isRead() {
      return 1 != (2097155 & this.flags);
    }
    get isWrite() {
      return !!(2097155 & this.flags);
    }
    get isAppend() {
      return 1024 & this.flags;
    }
    get flags() {
      return this.shared.flags;
    }
    set flags(val) {
      this.shared.flags = val;
    }
    get position() {
      return this.shared.position;
    }
    set position(val) {
      this.shared.position = val;
    }
  }, FSNode: class {
    constructor(parent, name, mode, rdev) {
      parent || (parent = this), this.parent = parent, this.mount = parent.mount, this.mounted = null, this.id = FS.nextInode++, this.name = name, this.mode = mode, this.node_ops = {}, this.stream_ops = {}, this.rdev = rdev, this.readMode = 365, this.writeMode = 146;
    }
    get read() {
      return (this.mode & this.readMode) === this.readMode;
    }
    set read(val) {
      val ? this.mode |= this.readMode : this.mode &= ~this.readMode;
    }
    get write() {
      return (this.mode & this.writeMode) === this.writeMode;
    }
    set write(val) {
      val ? this.mode |= this.writeMode : this.mode &= ~this.writeMode;
    }
    get isFolder() {
      return FS.isDir(this.mode);
    }
    get isDevice() {
      return FS.isChrdev(this.mode);
    }
  }, lookupPath(path, opts = {}) {
    if (!(path = PATH_FS.resolve(path))) return { path: "", node: null };
    if ((opts = Object.assign({ follow_mount: true, recurse_count: 0 }, opts)).recurse_count > 8) throw new FS.ErrnoError(32);
    for (var parts = path.split("/").filter((p) => !!p), current = FS.root, current_path = "/", i = 0; i < parts.length; i++) {
      var islast = i === parts.length - 1;
      if (islast && opts.parent) break;
      if (current = FS.lookupNode(current, parts[i]), current_path = PATH.join2(current_path, parts[i]), FS.isMountpoint(current) && (!islast || islast && opts.follow_mount) && (current = current.mounted.root), !islast || opts.follow) for (var count = 0; FS.isLink(current.mode); ) {
        var link = FS.readlink(current_path);
        if (current_path = PATH_FS.resolve(PATH.dirname(current_path), link), current = FS.lookupPath(current_path, { recurse_count: opts.recurse_count + 1 }).node, count++ > 40) throw new FS.ErrnoError(32);
      }
    }
    return { path: current_path, node: current };
  }, getPath(node) {
    for (var path; ; ) {
      if (FS.isRoot(node)) {
        var mount = node.mount.mountpoint;
        return path ? "/" !== mount[mount.length - 1] ? `${mount}/${path}` : mount + path : mount;
      }
      path = path ? `${node.name}/${path}` : node.name, node = node.parent;
    }
  }, hashName(parentid, name) {
    for (var hash = 0, i = 0; i < name.length; i++) hash = (hash << 5) - hash + name.charCodeAt(i) | 0;
    return (parentid + hash >>> 0) % FS.nameTable.length;
  }, hashAddNode(node) {
    var hash = FS.hashName(node.parent.id, node.name);
    node.name_next = FS.nameTable[hash], FS.nameTable[hash] = node;
  }, hashRemoveNode(node) {
    var hash = FS.hashName(node.parent.id, node.name);
    if (FS.nameTable[hash] === node) FS.nameTable[hash] = node.name_next;
    else for (var current = FS.nameTable[hash]; current; ) {
      if (current.name_next === node) {
        current.name_next = node.name_next;
        break;
      }
      current = current.name_next;
    }
  }, lookupNode(parent, name) {
    var errCode = FS.mayLookup(parent);
    if (errCode) throw new FS.ErrnoError(errCode);
    for (var hash = FS.hashName(parent.id, name), node = FS.nameTable[hash]; node; node = node.name_next) {
      var nodeName = node.name;
      if (node.parent.id === parent.id && nodeName === name) return node;
    }
    return FS.lookup(parent, name);
  }, createNode(parent, name, mode, rdev) {
    assert("object" == typeof parent);
    var node = new FS.FSNode(parent, name, mode, rdev);
    return FS.hashAddNode(node), node;
  }, destroyNode(node) {
    FS.hashRemoveNode(node);
  }, isRoot: (node) => node === node.parent, isMountpoint: (node) => !!node.mounted, isFile: (mode) => 32768 == (61440 & mode), isDir: (mode) => 16384 == (61440 & mode), isLink: (mode) => 40960 == (61440 & mode), isChrdev: (mode) => 8192 == (61440 & mode), isBlkdev: (mode) => 24576 == (61440 & mode), isFIFO: (mode) => 4096 == (61440 & mode), isSocket: (mode) => !(49152 & ~mode), flagsToPermissionString(flag) {
    var perms = ["r", "w", "rw"][3 & flag];
    return 512 & flag && (perms += "w"), perms;
  }, nodePermissions: (node, perms) => FS.ignorePermissions || (!perms.includes("r") || 292 & node.mode) && (!perms.includes("w") || 146 & node.mode) && (!perms.includes("x") || 73 & node.mode) ? 0 : 2, mayLookup(dir) {
    if (!FS.isDir(dir.mode)) return 54;
    var errCode = FS.nodePermissions(dir, "x");
    return errCode || (dir.node_ops.lookup ? 0 : 2);
  }, mayCreate(dir, name) {
    try {
      return FS.lookupNode(dir, name), 20;
    } catch (e) {
    }
    return FS.nodePermissions(dir, "wx");
  }, mayDelete(dir, name, isdir) {
    var node;
    try {
      node = FS.lookupNode(dir, name);
    } catch (e) {
      return e.errno;
    }
    var errCode = FS.nodePermissions(dir, "wx");
    if (errCode) return errCode;
    if (isdir) {
      if (!FS.isDir(node.mode)) return 54;
      if (FS.isRoot(node) || FS.getPath(node) === FS.cwd()) return 10;
    } else if (FS.isDir(node.mode)) return 31;
    return 0;
  }, mayOpen: (node, flags) => node ? FS.isLink(node.mode) ? 32 : FS.isDir(node.mode) && ("r" !== FS.flagsToPermissionString(flags) || 512 & flags) ? 31 : FS.nodePermissions(node, FS.flagsToPermissionString(flags)) : 44, MAX_OPEN_FDS: 4096, nextfd() {
    for (var fd = 0; fd <= FS.MAX_OPEN_FDS; fd++) if (!FS.streams[fd]) return fd;
    throw new FS.ErrnoError(33);
  }, getStreamChecked(fd) {
    var stream = FS.getStream(fd);
    if (!stream) throw new FS.ErrnoError(8);
    return stream;
  }, getStream: (fd) => FS.streams[fd], createStream: (stream, fd = -1) => (assert(fd >= -1), stream = Object.assign(new FS.FSStream(), stream), -1 == fd && (fd = FS.nextfd()), stream.fd = fd, FS.streams[fd] = stream, stream), closeStream(fd) {
    FS.streams[fd] = null;
  }, dupStream(origStream, fd = -1) {
    var stream = FS.createStream(origStream, fd);
    return stream.stream_ops?.dup?.(stream), stream;
  }, chrdev_stream_ops: { open(stream) {
    var device = FS.getDevice(stream.node.rdev);
    stream.stream_ops = device.stream_ops, stream.stream_ops.open?.(stream);
  }, llseek() {
    throw new FS.ErrnoError(70);
  } }, major: (dev) => dev >> 8, minor: (dev) => 255 & dev, makedev: (ma, mi) => ma << 8 | mi, registerDevice(dev, ops) {
    FS.devices[dev] = { stream_ops: ops };
  }, getDevice: (dev) => FS.devices[dev], getMounts(mount) {
    for (var mounts = [], check = [mount]; check.length; ) {
      var m = check.pop();
      mounts.push(m), check.push(...m.mounts);
    }
    return mounts;
  }, syncfs(populate, callback) {
    "function" == typeof populate && (callback = populate, populate = false), FS.syncFSRequests++, FS.syncFSRequests > 1 && err(`warning: ${FS.syncFSRequests} FS.syncfs operations in flight at once, probably just doing extra work`);
    var mounts = FS.getMounts(FS.root.mount), completed = 0;
    function doCallback(errCode) {
      return assert(FS.syncFSRequests > 0), FS.syncFSRequests--, callback(errCode);
    }
    function done(errCode) {
      if (errCode) return done.errored ? void 0 : (done.errored = true, doCallback(errCode));
      ++completed >= mounts.length && doCallback(null);
    }
    mounts.forEach((mount) => {
      if (!mount.type.syncfs) return done(null);
      mount.type.syncfs(mount, populate, done);
    });
  }, mount(type, opts, mountpoint) {
    if ("string" == typeof type) throw type;
    var node, root = "/" === mountpoint, pseudo = !mountpoint;
    if (root && FS.root) throw new FS.ErrnoError(10);
    if (!root && !pseudo) {
      var lookup = FS.lookupPath(mountpoint, { follow_mount: false });
      if (mountpoint = lookup.path, node = lookup.node, FS.isMountpoint(node)) throw new FS.ErrnoError(10);
      if (!FS.isDir(node.mode)) throw new FS.ErrnoError(54);
    }
    var mount = { type, opts, mountpoint, mounts: [] }, mountRoot = type.mount(mount);
    return mountRoot.mount = mount, mount.root = mountRoot, root ? FS.root = mountRoot : node && (node.mounted = mount, node.mount && node.mount.mounts.push(mount)), mountRoot;
  }, unmount(mountpoint) {
    var lookup = FS.lookupPath(mountpoint, { follow_mount: false });
    if (!FS.isMountpoint(lookup.node)) throw new FS.ErrnoError(28);
    var node = lookup.node, mount = node.mounted, mounts = FS.getMounts(mount);
    Object.keys(FS.nameTable).forEach((hash) => {
      for (var current = FS.nameTable[hash]; current; ) {
        var next = current.name_next;
        mounts.includes(current.mount) && FS.destroyNode(current), current = next;
      }
    }), node.mounted = null;
    var idx = node.mount.mounts.indexOf(mount);
    assert(-1 !== idx), node.mount.mounts.splice(idx, 1);
  }, lookup: (parent, name) => parent.node_ops.lookup(parent, name), mknod(path, mode, dev) {
    var parent = FS.lookupPath(path, { parent: true }).node, name = PATH.basename(path);
    if (!name || "." === name || ".." === name) throw new FS.ErrnoError(28);
    var errCode = FS.mayCreate(parent, name);
    if (errCode) throw new FS.ErrnoError(errCode);
    if (!parent.node_ops.mknod) throw new FS.ErrnoError(63);
    return parent.node_ops.mknod(parent, name, mode, dev);
  }, create: (path, mode) => (mode = void 0 !== mode ? mode : 438, mode &= 4095, mode |= 32768, FS.mknod(path, mode, 0)), mkdir: (path, mode) => (mode = void 0 !== mode ? mode : 511, mode &= 1023, mode |= 16384, FS.mknod(path, mode, 0)), mkdirTree(path, mode) {
    for (var dirs = path.split("/"), d = "", i = 0; i < dirs.length; ++i) if (dirs[i]) {
      d += "/" + dirs[i];
      try {
        FS.mkdir(d, mode);
      } catch (e) {
        if (20 != e.errno) throw e;
      }
    }
  }, mkdev: (path, mode, dev) => (void 0 === dev && (dev = mode, mode = 438), mode |= 8192, FS.mknod(path, mode, dev)), symlink(oldpath, newpath) {
    if (!PATH_FS.resolve(oldpath)) throw new FS.ErrnoError(44);
    var parent = FS.lookupPath(newpath, { parent: true }).node;
    if (!parent) throw new FS.ErrnoError(44);
    var newname = PATH.basename(newpath), errCode = FS.mayCreate(parent, newname);
    if (errCode) throw new FS.ErrnoError(errCode);
    if (!parent.node_ops.symlink) throw new FS.ErrnoError(63);
    return parent.node_ops.symlink(parent, newname, oldpath);
  }, rename(old_path, new_path) {
    var old_dir, new_dir, old_dirname = PATH.dirname(old_path), new_dirname = PATH.dirname(new_path), old_name = PATH.basename(old_path), new_name = PATH.basename(new_path);
    if (old_dir = FS.lookupPath(old_path, { parent: true }).node, new_dir = FS.lookupPath(new_path, { parent: true }).node, !old_dir || !new_dir) throw new FS.ErrnoError(44);
    if (old_dir.mount !== new_dir.mount) throw new FS.ErrnoError(75);
    var new_node, old_node = FS.lookupNode(old_dir, old_name), relative = PATH_FS.relative(old_path, new_dirname);
    if ("." !== relative.charAt(0)) throw new FS.ErrnoError(28);
    if ("." !== (relative = PATH_FS.relative(new_path, old_dirname)).charAt(0)) throw new FS.ErrnoError(55);
    try {
      new_node = FS.lookupNode(new_dir, new_name);
    } catch (e) {
    }
    if (old_node !== new_node) {
      var isdir = FS.isDir(old_node.mode), errCode = FS.mayDelete(old_dir, old_name, isdir);
      if (errCode) throw new FS.ErrnoError(errCode);
      if (errCode = new_node ? FS.mayDelete(new_dir, new_name, isdir) : FS.mayCreate(new_dir, new_name)) throw new FS.ErrnoError(errCode);
      if (!old_dir.node_ops.rename) throw new FS.ErrnoError(63);
      if (FS.isMountpoint(old_node) || new_node && FS.isMountpoint(new_node)) throw new FS.ErrnoError(10);
      if (new_dir !== old_dir && (errCode = FS.nodePermissions(old_dir, "w"))) throw new FS.ErrnoError(errCode);
      FS.hashRemoveNode(old_node);
      try {
        old_dir.node_ops.rename(old_node, new_dir, new_name), old_node.parent = new_dir;
      } catch (e) {
        throw e;
      } finally {
        FS.hashAddNode(old_node);
      }
    }
  }, rmdir(path) {
    var parent = FS.lookupPath(path, { parent: true }).node, name = PATH.basename(path), node = FS.lookupNode(parent, name), errCode = FS.mayDelete(parent, name, true);
    if (errCode) throw new FS.ErrnoError(errCode);
    if (!parent.node_ops.rmdir) throw new FS.ErrnoError(63);
    if (FS.isMountpoint(node)) throw new FS.ErrnoError(10);
    parent.node_ops.rmdir(parent, name), FS.destroyNode(node);
  }, readdir(path) {
    var node = FS.lookupPath(path, { follow: true }).node;
    if (!node.node_ops.readdir) throw new FS.ErrnoError(54);
    return node.node_ops.readdir(node);
  }, unlink(path) {
    var parent = FS.lookupPath(path, { parent: true }).node;
    if (!parent) throw new FS.ErrnoError(44);
    var name = PATH.basename(path), node = FS.lookupNode(parent, name), errCode = FS.mayDelete(parent, name, false);
    if (errCode) throw new FS.ErrnoError(errCode);
    if (!parent.node_ops.unlink) throw new FS.ErrnoError(63);
    if (FS.isMountpoint(node)) throw new FS.ErrnoError(10);
    parent.node_ops.unlink(parent, name), FS.destroyNode(node);
  }, readlink(path) {
    var link = FS.lookupPath(path).node;
    if (!link) throw new FS.ErrnoError(44);
    if (!link.node_ops.readlink) throw new FS.ErrnoError(28);
    return PATH_FS.resolve(FS.getPath(link.parent), link.node_ops.readlink(link));
  }, stat(path, dontFollow) {
    var node = FS.lookupPath(path, { follow: !dontFollow }).node;
    if (!node) throw new FS.ErrnoError(44);
    if (!node.node_ops.getattr) throw new FS.ErrnoError(63);
    return node.node_ops.getattr(node);
  }, lstat: (path) => FS.stat(path, true), chmod(path, mode, dontFollow) {
    var node;
    if (!(node = "string" == typeof path ? FS.lookupPath(path, { follow: !dontFollow }).node : path).node_ops.setattr) throw new FS.ErrnoError(63);
    node.node_ops.setattr(node, { mode: 4095 & mode | -4096 & node.mode, timestamp: Date.now() });
  }, lchmod(path, mode) {
    FS.chmod(path, mode, true);
  }, fchmod(fd, mode) {
    var stream = FS.getStreamChecked(fd);
    FS.chmod(stream.node, mode);
  }, chown(path, uid, gid, dontFollow) {
    var node;
    if (!(node = "string" == typeof path ? FS.lookupPath(path, { follow: !dontFollow }).node : path).node_ops.setattr) throw new FS.ErrnoError(63);
    node.node_ops.setattr(node, { timestamp: Date.now() });
  }, lchown(path, uid, gid) {
    FS.chown(path, uid, gid, true);
  }, fchown(fd, uid, gid) {
    var stream = FS.getStreamChecked(fd);
    FS.chown(stream.node, uid, gid);
  }, truncate(path, len) {
    if (len < 0) throw new FS.ErrnoError(28);
    var node;
    if (!(node = "string" == typeof path ? FS.lookupPath(path, { follow: true }).node : path).node_ops.setattr) throw new FS.ErrnoError(63);
    if (FS.isDir(node.mode)) throw new FS.ErrnoError(31);
    if (!FS.isFile(node.mode)) throw new FS.ErrnoError(28);
    var errCode = FS.nodePermissions(node, "w");
    if (errCode) throw new FS.ErrnoError(errCode);
    node.node_ops.setattr(node, { size: len, timestamp: Date.now() });
  }, ftruncate(fd, len) {
    var stream = FS.getStreamChecked(fd);
    if (!(2097155 & stream.flags)) throw new FS.ErrnoError(28);
    FS.truncate(stream.node, len);
  }, utime(path, atime, mtime) {
    var node = FS.lookupPath(path, { follow: true }).node;
    node.node_ops.setattr(node, { timestamp: Math.max(atime, mtime) });
  }, open(path, flags, mode) {
    if ("" === path) throw new FS.ErrnoError(44);
    var node;
    if (mode = 64 & (flags = "string" == typeof flags ? ((str) => {
      var flags2 = { r: 0, "r+": 2, w: 577, "w+": 578, a: 1089, "a+": 1090 }[str];
      if (void 0 === flags2) throw new Error(`Unknown file open mode: ${str}`);
      return flags2;
    })(flags) : flags) ? 4095 & (mode = void 0 === mode ? 438 : mode) | 32768 : 0, "object" == typeof path) node = path;
    else {
      path = PATH.normalize(path);
      try {
        node = FS.lookupPath(path, { follow: !(131072 & flags) }).node;
      } catch (e) {
      }
    }
    var created = false;
    if (64 & flags) if (node) {
      if (128 & flags) throw new FS.ErrnoError(20);
    } else node = FS.mknod(path, mode, 0), created = true;
    if (!node) throw new FS.ErrnoError(44);
    if (FS.isChrdev(node.mode) && (flags &= -513), 65536 & flags && !FS.isDir(node.mode)) throw new FS.ErrnoError(54);
    if (!created) {
      var errCode = FS.mayOpen(node, flags);
      if (errCode) throw new FS.ErrnoError(errCode);
    }
    512 & flags && !created && FS.truncate(node, 0), flags &= -131713;
    var stream = FS.createStream({ node, path: FS.getPath(node), flags, seekable: true, position: 0, stream_ops: node.stream_ops, ungotten: [], error: false });
    return stream.stream_ops.open && stream.stream_ops.open(stream), !Module2.logReadFiles || 1 & flags || (FS.readFiles || (FS.readFiles = {}), path in FS.readFiles || (FS.readFiles[path] = 1)), stream;
  }, close(stream) {
    if (FS.isClosed(stream)) throw new FS.ErrnoError(8);
    stream.getdents && (stream.getdents = null);
    try {
      stream.stream_ops.close && stream.stream_ops.close(stream);
    } catch (e) {
      throw e;
    } finally {
      FS.closeStream(stream.fd);
    }
    stream.fd = null;
  }, isClosed: (stream) => null === stream.fd, llseek(stream, offset, whence) {
    if (FS.isClosed(stream)) throw new FS.ErrnoError(8);
    if (!stream.seekable || !stream.stream_ops.llseek) throw new FS.ErrnoError(70);
    if (0 != whence && 1 != whence && 2 != whence) throw new FS.ErrnoError(28);
    return stream.position = stream.stream_ops.llseek(stream, offset, whence), stream.ungotten = [], stream.position;
  }, read(stream, buffer, offset, length, position) {
    if (assert(offset >= 0), length < 0 || position < 0) throw new FS.ErrnoError(28);
    if (FS.isClosed(stream)) throw new FS.ErrnoError(8);
    if (1 == (2097155 & stream.flags)) throw new FS.ErrnoError(8);
    if (FS.isDir(stream.node.mode)) throw new FS.ErrnoError(31);
    if (!stream.stream_ops.read) throw new FS.ErrnoError(28);
    var seeking = void 0 !== position;
    if (seeking) {
      if (!stream.seekable) throw new FS.ErrnoError(70);
    } else position = stream.position;
    var bytesRead = stream.stream_ops.read(stream, buffer, offset, length, position);
    return seeking || (stream.position += bytesRead), bytesRead;
  }, write(stream, buffer, offset, length, position, canOwn) {
    if (assert(offset >= 0), length < 0 || position < 0) throw new FS.ErrnoError(28);
    if (FS.isClosed(stream)) throw new FS.ErrnoError(8);
    if (!(2097155 & stream.flags)) throw new FS.ErrnoError(8);
    if (FS.isDir(stream.node.mode)) throw new FS.ErrnoError(31);
    if (!stream.stream_ops.write) throw new FS.ErrnoError(28);
    stream.seekable && 1024 & stream.flags && FS.llseek(stream, 0, 2);
    var seeking = void 0 !== position;
    if (seeking) {
      if (!stream.seekable) throw new FS.ErrnoError(70);
    } else position = stream.position;
    var bytesWritten = stream.stream_ops.write(stream, buffer, offset, length, position, canOwn);
    return seeking || (stream.position += bytesWritten), bytesWritten;
  }, allocate(stream, offset, length) {
    if (FS.isClosed(stream)) throw new FS.ErrnoError(8);
    if (offset < 0 || length <= 0) throw new FS.ErrnoError(28);
    if (!(2097155 & stream.flags)) throw new FS.ErrnoError(8);
    if (!FS.isFile(stream.node.mode) && !FS.isDir(stream.node.mode)) throw new FS.ErrnoError(43);
    if (!stream.stream_ops.allocate) throw new FS.ErrnoError(138);
    stream.stream_ops.allocate(stream, offset, length);
  }, mmap(stream, length, position, prot, flags) {
    if (2 & prot && !(2 & flags) && 2 != (2097155 & stream.flags)) throw new FS.ErrnoError(2);
    if (1 == (2097155 & stream.flags)) throw new FS.ErrnoError(2);
    if (!stream.stream_ops.mmap) throw new FS.ErrnoError(43);
    if (!length) throw new FS.ErrnoError(28);
    return stream.stream_ops.mmap(stream, length, position, prot, flags);
  }, msync: (stream, buffer, offset, length, mmapFlags) => (assert(offset >= 0), stream.stream_ops.msync ? stream.stream_ops.msync(stream, buffer, offset, length, mmapFlags) : 0), ioctl(stream, cmd, arg) {
    if (!stream.stream_ops.ioctl) throw new FS.ErrnoError(59);
    return stream.stream_ops.ioctl(stream, cmd, arg);
  }, readFile(path, opts = {}) {
    if (opts.flags = opts.flags || 0, opts.encoding = opts.encoding || "binary", "utf8" !== opts.encoding && "binary" !== opts.encoding) throw new Error(`Invalid encoding type "${opts.encoding}"`);
    var ret, stream = FS.open(path, opts.flags), length = FS.stat(path).size, buf = new Uint8Array(length);
    return FS.read(stream, buf, 0, length, 0), "utf8" === opts.encoding ? ret = UTF8ArrayToString(buf, 0) : "binary" === opts.encoding && (ret = buf), FS.close(stream), ret;
  }, writeFile(path, data, opts = {}) {
    opts.flags = opts.flags || 577;
    var stream = FS.open(path, opts.flags, opts.mode);
    if ("string" == typeof data) {
      var buf = new Uint8Array(lengthBytesUTF8(data) + 1), actualNumBytes = stringToUTF8Array(data, buf, 0, buf.length);
      FS.write(stream, buf, 0, actualNumBytes, void 0, opts.canOwn);
    } else {
      if (!ArrayBuffer.isView(data)) throw new Error("Unsupported data type");
      FS.write(stream, data, 0, data.byteLength, void 0, opts.canOwn);
    }
    FS.close(stream);
  }, cwd: () => FS.currentPath, chdir(path) {
    var lookup = FS.lookupPath(path, { follow: true });
    if (null === lookup.node) throw new FS.ErrnoError(44);
    if (!FS.isDir(lookup.node.mode)) throw new FS.ErrnoError(54);
    var errCode = FS.nodePermissions(lookup.node, "x");
    if (errCode) throw new FS.ErrnoError(errCode);
    FS.currentPath = lookup.path;
  }, createDefaultDirectories() {
    FS.mkdir("/tmp"), FS.mkdir("/home"), FS.mkdir("/home/web_user");
  }, createDefaultDevices() {
    FS.mkdir("/dev"), FS.registerDevice(FS.makedev(1, 3), { read: () => 0, write: (stream, buffer, offset, length, pos) => length }), FS.mkdev("/dev/null", FS.makedev(1, 3)), TTY.register(FS.makedev(5, 0), TTY.default_tty_ops), TTY.register(FS.makedev(6, 0), TTY.default_tty1_ops), FS.mkdev("/dev/tty", FS.makedev(5, 0)), FS.mkdev("/dev/tty1", FS.makedev(6, 0));
    var randomBuffer = new Uint8Array(1024), randomLeft = 0, randomByte = () => (0 === randomLeft && (randomLeft = randomFill(randomBuffer).byteLength), randomBuffer[--randomLeft]);
    FS.createDevice("/dev", "random", randomByte), FS.createDevice("/dev", "urandom", randomByte), FS.mkdir("/dev/shm"), FS.mkdir("/dev/shm/tmp");
  }, createSpecialDirectories() {
    FS.mkdir("/proc");
    var proc_self = FS.mkdir("/proc/self");
    FS.mkdir("/proc/self/fd"), FS.mount({ mount() {
      var node = FS.createNode(proc_self, "fd", 16895, 73);
      return node.node_ops = { lookup(parent, name) {
        var fd = +name, stream = FS.getStreamChecked(fd), ret = { parent: null, mount: { mountpoint: "fake" }, node_ops: { readlink: () => stream.path } };
        return ret.parent = ret, ret;
      } }, node;
    } }, {}, "/proc/self/fd");
  }, createStandardStreams(input, output, error) {
    input ? FS.createDevice("/dev", "stdin", input) : FS.symlink("/dev/tty", "/dev/stdin"), output ? FS.createDevice("/dev", "stdout", null, output) : FS.symlink("/dev/tty", "/dev/stdout"), error ? FS.createDevice("/dev", "stderr", null, error) : FS.symlink("/dev/tty1", "/dev/stderr");
    var stdin = FS.open("/dev/stdin", 0), stdout = FS.open("/dev/stdout", 1), stderr = FS.open("/dev/stderr", 1);
    assert(0 === stdin.fd, `invalid handle for stdin (${stdin.fd})`), assert(1 === stdout.fd, `invalid handle for stdout (${stdout.fd})`), assert(2 === stderr.fd, `invalid handle for stderr (${stderr.fd})`);
  }, staticInit() {
    [44].forEach((code) => {
      FS.genericErrors[code] = new FS.ErrnoError(code), FS.genericErrors[code].stack = "<generic error, no stack>";
    }), FS.nameTable = new Array(4096), FS.mount(MEMFS, {}, "/"), FS.createDefaultDirectories(), FS.createDefaultDevices(), FS.createSpecialDirectories(), FS.filesystems = { MEMFS };
  }, init(input, output, error) {
    assert(!FS.initialized, "FS.init was previously called. If you want to initialize later with custom parameters, remove any earlier calls (note that one is automatically added to the generated code)"), FS.initialized = true, input ??= Module2.stdin, output ??= Module2.stdout, error ??= Module2.stderr, FS.createStandardStreams(input, output, error);
  }, quit() {
    FS.initialized = false, _fflush(0);
    for (var i = 0; i < FS.streams.length; i++) {
      var stream = FS.streams[i];
      stream && FS.close(stream);
    }
  }, findObject(path, dontResolveLastLink) {
    var ret = FS.analyzePath(path, dontResolveLastLink);
    return ret.exists ? ret.object : null;
  }, analyzePath(path, dontResolveLastLink) {
    try {
      path = (lookup = FS.lookupPath(path, { follow: !dontResolveLastLink })).path;
    } catch (e) {
    }
    var ret = { isRoot: false, exists: false, error: 0, name: null, path: null, object: null, parentExists: false, parentPath: null, parentObject: null };
    try {
      var lookup = FS.lookupPath(path, { parent: true });
      ret.parentExists = true, ret.parentPath = lookup.path, ret.parentObject = lookup.node, ret.name = PATH.basename(path), lookup = FS.lookupPath(path, { follow: !dontResolveLastLink }), ret.exists = true, ret.path = lookup.path, ret.object = lookup.node, ret.name = lookup.node.name, ret.isRoot = "/" === lookup.path;
    } catch (e) {
      ret.error = e.errno;
    }
    return ret;
  }, createPath(parent, path, canRead, canWrite) {
    parent = "string" == typeof parent ? parent : FS.getPath(parent);
    for (var parts = path.split("/").reverse(); parts.length; ) {
      var part = parts.pop();
      if (part) {
        var current = PATH.join2(parent, part);
        try {
          FS.mkdir(current);
        } catch (e) {
        }
        parent = current;
      }
    }
    return current;
  }, createFile(parent, name, properties, canRead, canWrite) {
    var path = PATH.join2("string" == typeof parent ? parent : FS.getPath(parent), name), mode = FS_getMode(canRead, canWrite);
    return FS.create(path, mode);
  }, createDataFile(parent, name, data, canRead, canWrite, canOwn) {
    var path = name;
    parent && (parent = "string" == typeof parent ? parent : FS.getPath(parent), path = name ? PATH.join2(parent, name) : parent);
    var mode = FS_getMode(canRead, canWrite), node = FS.create(path, mode);
    if (data) {
      if ("string" == typeof data) {
        for (var arr = new Array(data.length), i = 0, len = data.length; i < len; ++i) arr[i] = data.charCodeAt(i);
        data = arr;
      }
      FS.chmod(node, 146 | mode);
      var stream = FS.open(node, 577);
      FS.write(stream, data, 0, data.length, 0, canOwn), FS.close(stream), FS.chmod(node, mode);
    }
  }, createDevice(parent, name, input, output) {
    var path = PATH.join2("string" == typeof parent ? parent : FS.getPath(parent), name), mode = FS_getMode(!!input, !!output);
    FS.createDevice.major || (FS.createDevice.major = 64);
    var dev = FS.makedev(FS.createDevice.major++, 0);
    return FS.registerDevice(dev, { open(stream) {
      stream.seekable = false;
    }, close(stream) {
      output?.buffer?.length && output(10);
    }, read(stream, buffer, offset, length, pos) {
      for (var bytesRead = 0, i = 0; i < length; i++) {
        var result;
        try {
          result = input();
        } catch (e) {
          throw new FS.ErrnoError(29);
        }
        if (void 0 === result && 0 === bytesRead) throw new FS.ErrnoError(6);
        if (null == result) break;
        bytesRead++, buffer[offset + i] = result;
      }
      return bytesRead && (stream.node.timestamp = Date.now()), bytesRead;
    }, write(stream, buffer, offset, length, pos) {
      for (var i = 0; i < length; i++) try {
        output(buffer[offset + i]);
      } catch (e) {
        throw new FS.ErrnoError(29);
      }
      return length && (stream.node.timestamp = Date.now()), i;
    } }), FS.mkdev(path, mode, dev);
  }, forceLoadFile(obj) {
    if (obj.isDevice || obj.isFolder || obj.link || obj.contents) return true;
    if ("undefined" != typeof XMLHttpRequest) throw new Error("Lazy loading should have been performed (contents set) in createLazyFile, but it was not. Lazy loading only works in web workers. Use --embed-file or --preload-file in emcc on the main thread.");
    try {
      obj.contents = readBinary(obj.url), obj.usedBytes = obj.contents.length;
    } catch (e) {
      throw new FS.ErrnoError(29);
    }
  }, createLazyFile(parent, name, url, canRead, canWrite) {
    class LazyUint8Array {
      constructor() {
        this.lengthKnown = false, this.chunks = [];
      }
      get(idx) {
        if (!(idx > this.length - 1 || idx < 0)) {
          var chunkOffset = idx % this.chunkSize, chunkNum = idx / this.chunkSize | 0;
          return this.getter(chunkNum)[chunkOffset];
        }
      }
      setDataGetter(getter) {
        this.getter = getter;
      }
      cacheLength() {
        var xhr = new XMLHttpRequest();
        if (xhr.open("HEAD", url, false), xhr.send(null), !(xhr.status >= 200 && xhr.status < 300 || 304 === xhr.status)) throw new Error("Couldn't load " + url + ". Status: " + xhr.status);
        var header, datalength = Number(xhr.getResponseHeader("Content-length")), hasByteServing = (header = xhr.getResponseHeader("Accept-Ranges")) && "bytes" === header, usesGzip = (header = xhr.getResponseHeader("Content-Encoding")) && "gzip" === header, chunkSize = 1048576;
        hasByteServing || (chunkSize = datalength);
        var lazyArray = this;
        lazyArray.setDataGetter((chunkNum) => {
          var start = chunkNum * chunkSize, end = (chunkNum + 1) * chunkSize - 1;
          if (end = Math.min(end, datalength - 1), void 0 === lazyArray.chunks[chunkNum] && (lazyArray.chunks[chunkNum] = ((from, to) => {
            if (from > to) throw new Error("invalid range (" + from + ", " + to + ") or no bytes requested!");
            if (to > datalength - 1) throw new Error("only " + datalength + " bytes available! programmer error!");
            var xhr2 = new XMLHttpRequest();
            if (xhr2.open("GET", url, false), datalength !== chunkSize && xhr2.setRequestHeader("Range", "bytes=" + from + "-" + to), xhr2.responseType = "arraybuffer", xhr2.overrideMimeType && xhr2.overrideMimeType("text/plain; charset=x-user-defined"), xhr2.send(null), !(xhr2.status >= 200 && xhr2.status < 300 || 304 === xhr2.status)) throw new Error("Couldn't load " + url + ". Status: " + xhr2.status);
            return void 0 !== xhr2.response ? new Uint8Array(xhr2.response || []) : intArrayFromString(xhr2.responseText || "", true);
          })(start, end)), void 0 === lazyArray.chunks[chunkNum]) throw new Error("doXHR failed!");
          return lazyArray.chunks[chunkNum];
        }), !usesGzip && datalength || (chunkSize = datalength = 1, datalength = this.getter(0).length, chunkSize = datalength, out("LazyFiles on gzip forces download of the whole file when length is accessed")), this._length = datalength, this._chunkSize = chunkSize, this.lengthKnown = true;
      }
      get length() {
        return this.lengthKnown || this.cacheLength(), this._length;
      }
      get chunkSize() {
        return this.lengthKnown || this.cacheLength(), this._chunkSize;
      }
    }
    if ("undefined" != typeof XMLHttpRequest) {
      if (!ENVIRONMENT_IS_WORKER) throw "Cannot do synchronous binary XHRs outside webworkers in modern browsers. Use --embed-file or --preload-file in emcc";
      var properties = { isDevice: false, contents: new LazyUint8Array() };
    } else properties = { isDevice: false, url };
    var node = FS.createFile(parent, name, properties, canRead, canWrite);
    properties.contents ? node.contents = properties.contents : properties.url && (node.contents = null, node.url = properties.url), Object.defineProperties(node, { usedBytes: { get: function() {
      return this.contents.length;
    } } });
    var stream_ops = {};
    function writeChunks(stream, buffer, offset, length, position) {
      var contents = stream.node.contents;
      if (position >= contents.length) return 0;
      var size = Math.min(contents.length - position, length);
      if (assert(size >= 0), contents.slice) for (var i = 0; i < size; i++) buffer[offset + i] = contents[position + i];
      else for (i = 0; i < size; i++) buffer[offset + i] = contents.get(position + i);
      return size;
    }
    return Object.keys(node.stream_ops).forEach((key) => {
      var fn = node.stream_ops[key];
      stream_ops[key] = (...args) => (FS.forceLoadFile(node), fn(...args));
    }), stream_ops.read = (stream, buffer, offset, length, position) => (FS.forceLoadFile(node), writeChunks(stream, buffer, offset, length, position)), stream_ops.mmap = (stream, length, position, prot, flags) => {
      FS.forceLoadFile(node);
      var ptr = mmapAlloc();
      if (!ptr) throw new FS.ErrnoError(48);
      return writeChunks(stream, HEAP8, ptr, length, position), { ptr, allocated: true };
    }, node.stream_ops = stream_ops, node;
  }, absolutePath() {
    abort("FS.absolutePath has been removed; use PATH_FS.resolve instead");
  }, createFolder() {
    abort("FS.createFolder has been removed; use FS.mkdir instead");
  }, createLink() {
    abort("FS.createLink has been removed; use FS.symlink instead");
  }, joinPath() {
    abort("FS.joinPath has been removed; use PATH.join instead");
  }, mmapAlloc() {
    abort("FS.mmapAlloc has been replaced by the top level function mmapAlloc");
  }, standardizePath() {
    abort("FS.standardizePath has been removed; use PATH.normalize instead");
  } }, SYSCALLS = { DEFAULT_POLLMASK: 5, calculateAt(dirfd, path, allowEmpty) {
    if (PATH.isAbs(path)) return path;
    var dir;
    if (dir = -100 === dirfd ? FS.cwd() : SYSCALLS.getStreamFromFD(dirfd).path, 0 == path.length) {
      if (!allowEmpty) throw new FS.ErrnoError(44);
      return dir;
    }
    return PATH.join2(dir, path);
  }, doStat(func, path, buf) {
    var stat = func(path);
    HEAP32[buf >> 2] = stat.dev, HEAP32[buf + 4 >> 2] = stat.mode, HEAPU32[buf + 8 >> 2] = stat.nlink, HEAP32[buf + 12 >> 2] = stat.uid, HEAP32[buf + 16 >> 2] = stat.gid, HEAP32[buf + 20 >> 2] = stat.rdev, tempI64 = [stat.size >>> 0, (tempDouble = stat.size, +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[buf + 24 >> 2] = tempI64[0], HEAP32[buf + 28 >> 2] = tempI64[1], HEAP32[buf + 32 >> 2] = 4096, HEAP32[buf + 36 >> 2] = stat.blocks;
    var atime = stat.atime.getTime(), mtime = stat.mtime.getTime(), ctime = stat.ctime.getTime();
    return tempI64 = [Math.floor(atime / 1e3) >>> 0, (tempDouble = Math.floor(atime / 1e3), +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[buf + 40 >> 2] = tempI64[0], HEAP32[buf + 44 >> 2] = tempI64[1], HEAPU32[buf + 48 >> 2] = atime % 1e3 * 1e3 * 1e3, tempI64 = [Math.floor(mtime / 1e3) >>> 0, (tempDouble = Math.floor(mtime / 1e3), +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[buf + 56 >> 2] = tempI64[0], HEAP32[buf + 60 >> 2] = tempI64[1], HEAPU32[buf + 64 >> 2] = mtime % 1e3 * 1e3 * 1e3, tempI64 = [Math.floor(ctime / 1e3) >>> 0, (tempDouble = Math.floor(ctime / 1e3), +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[buf + 72 >> 2] = tempI64[0], HEAP32[buf + 76 >> 2] = tempI64[1], HEAPU32[buf + 80 >> 2] = ctime % 1e3 * 1e3 * 1e3, tempI64 = [stat.ino >>> 0, (tempDouble = stat.ino, +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[buf + 88 >> 2] = tempI64[0], HEAP32[buf + 92 >> 2] = tempI64[1], 0;
  }, doMsync(addr, stream, len, flags, offset) {
    if (!FS.isFile(stream.node.mode)) throw new FS.ErrnoError(43);
    if (2 & flags) return 0;
    var buffer = HEAPU8.slice(addr, addr + len);
    FS.msync(stream, buffer, offset, len, flags);
  }, getStreamFromFD: (fd) => FS.getStreamChecked(fd), varargs: void 0, getStr: (ptr) => UTF8ToString(ptr) }, stringToUTF8 = (str, outPtr, maxBytesToWrite) => (assert("number" == typeof maxBytesToWrite, "stringToUTF8(str, outPtr, maxBytesToWrite) is missing the third parameter that specifies the length of the output buffer!"), stringToUTF8Array(str, HEAPU8, outPtr, maxBytesToWrite)), growMemory = (size) => {
    var b = wasmMemory.buffer, pages = (size - b.byteLength + 65535) / 65536;
    try {
      return wasmMemory.grow(pages), updateMemoryViews(), 1;
    } catch (e) {
      err(`growMemory: Attempted to grow heap from ${b.byteLength} bytes to ${size} bytes, but got error: ${e}`);
    }
  }, wasmTableMirror = [], getWasmTableEntry = (funcPtr) => {
    var func = wasmTableMirror[funcPtr];
    return func || (funcPtr >= wasmTableMirror.length && (wasmTableMirror.length = funcPtr + 1), wasmTableMirror[funcPtr] = func = wasmTable.get(funcPtr)), assert(wasmTable.get(funcPtr) == func, "JavaScript-side Wasm function table mirror is out of date!"), func;
  }, stackAlloc = (sz) => __emscripten_stack_alloc(sz), ccall = (ident, returnType, argTypes, args, opts) => {
    var toC = { string: (str) => {
      var ret2 = 0;
      return null != str && 0 !== str && (ret2 = ((str2) => {
        var size = lengthBytesUTF8(str2) + 1, ret3 = stackAlloc(size);
        return stringToUTF8(str2, ret3, size), ret3;
      })(str)), ret2;
    }, array: (arr) => {
      var array, buffer, ret2 = stackAlloc(arr.length);
      return buffer = ret2, assert((array = arr).length >= 0, "writeArrayToMemory array must have a length (should be an array or typed array)"), HEAP8.set(array, buffer), ret2;
    } }, func = ((ident2) => {
      var func2 = Module2["_" + ident2];
      return assert(func2, "Cannot call unknown function " + ident2 + ", make sure it is exported"), func2;
    })(ident), cArgs = [], stack = 0;
    if (assert("array" !== returnType, 'Return type should not be "array".'), args) for (var i = 0; i < args.length; i++) {
      var converter = toC[argTypes[i]];
      converter ? (0 === stack && (stack = stackSave()), cArgs[i] = converter(args[i])) : cArgs[i] = args[i];
    }
    var ret = func(...cArgs);
    return ret = function(ret2) {
      return 0 !== stack && stackRestore(stack), function(ret3) {
        return "string" === returnType ? UTF8ToString(ret3) : "boolean" === returnType ? Boolean(ret3) : ret3;
      }(ret2);
    }(ret);
  };
  FS.createPreloadedFile = (parent, name, url, canRead, canWrite, onload, onerror, dontCreateFile, canOwn, preFinish) => {
    var fullname = name ? PATH_FS.resolve(PATH.join2(parent, name)) : parent, dep = getUniqueRunDependency(`cp ${fullname}`);
    function processData(byteArray) {
      function finish(byteArray2) {
        preFinish?.(), dontCreateFile || ((parent2, name2, fileData, canRead2, canWrite2, canOwn2) => {
          FS.createDataFile(parent2, name2, fileData, canRead2, canWrite2, canOwn2);
        })(parent, name, byteArray2, canRead, canWrite, canOwn), onload?.(), removeRunDependency(dep);
      }
      ((byteArray2, fullname2, finish2, onerror2) => {
        "undefined" != typeof Browser && Browser.init();
        var handled = false;
        return preloadPlugins.forEach((plugin) => {
          handled || plugin.canHandle(fullname2) && (plugin.handle(byteArray2, fullname2, finish2, onerror2), handled = true);
        }), handled;
      })(byteArray, fullname, finish, () => {
        onerror?.(), removeRunDependency(dep);
      }) || finish(byteArray);
    }
    addRunDependency(dep), "string" == typeof url ? ((url2, onload2, onerror2, noRunDep) => {
      var dep2 = noRunDep ? "" : getUniqueRunDependency(`al ${url2}`);
      readAsync(url2).then((arrayBuffer) => {
        assert(arrayBuffer, `Loading data file "${url2}" failed (no arrayBuffer).`), onload2(new Uint8Array(arrayBuffer)), dep2 && removeRunDependency(dep2);
      }, (err2) => {
        if (!onerror2) throw `Loading data file "${url2}" failed.`;
        onerror2();
      }), dep2 && addRunDependency(dep2);
    })(url, processData, onerror) : processData(url);
  }, FS.staticInit(), void 0 === globalThis.crypto && (globalThis.crypto = require2("crypto"));
  var calledRun, MP_JS_EPOCH = Date.now(), wasmImports = { __syscall_chdir: function(path) {
    try {
      return path = SYSCALLS.getStr(path), FS.chdir(path), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_fstat64: function(fd, buf) {
    try {
      var stream = SYSCALLS.getStreamFromFD(fd);
      return SYSCALLS.doStat(FS.stat, stream.path, buf);
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_getcwd: function(buf, size) {
    try {
      if (0 === size) return -28;
      var cwd = FS.cwd(), cwdLengthInBytes = lengthBytesUTF8(cwd) + 1;
      return size < cwdLengthInBytes ? -68 : (stringToUTF8(cwd, buf, size), cwdLengthInBytes);
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_getdents64: function(fd, dirp, count) {
    try {
      var stream = SYSCALLS.getStreamFromFD(fd);
      stream.getdents ||= FS.readdir(stream.path);
      for (var pos = 0, off = FS.llseek(stream, 0, 1), idx = Math.floor(off / 280); idx < stream.getdents.length && pos + 280 <= count; ) {
        var id, type, name = stream.getdents[idx];
        if ("." === name) id = stream.node.id, type = 4;
        else if (".." === name) id = FS.lookupPath(stream.path, { parent: true }).node.id, type = 4;
        else {
          var child = FS.lookupNode(stream.node, name);
          id = child.id, type = FS.isChrdev(child.mode) ? 2 : FS.isDir(child.mode) ? 4 : FS.isLink(child.mode) ? 10 : 8;
        }
        assert(id), tempI64 = [id >>> 0, (tempDouble = id, +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[dirp + pos >> 2] = tempI64[0], HEAP32[dirp + pos + 4 >> 2] = tempI64[1], tempI64 = [280 * (idx + 1) >>> 0, (tempDouble = 280 * (idx + 1), +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[dirp + pos + 8 >> 2] = tempI64[0], HEAP32[dirp + pos + 12 >> 2] = tempI64[1], HEAP16[dirp + pos + 16 >> 1] = 280, HEAP8[dirp + pos + 18] = type, stringToUTF8(name, dirp + pos + 19, 256), pos += 280, idx += 1;
      }
      return FS.llseek(stream, 280 * idx, 0), pos;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_lstat64: function(path, buf) {
    try {
      return path = SYSCALLS.getStr(path), SYSCALLS.doStat(FS.lstat, path, buf);
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_mkdirat: function(dirfd, path, mode) {
    try {
      return path = SYSCALLS.getStr(path), path = SYSCALLS.calculateAt(dirfd, path), "/" === (path = PATH.normalize(path))[path.length - 1] && (path = path.substr(0, path.length - 1)), FS.mkdir(path, mode, 0), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_newfstatat: function(dirfd, path, buf, flags) {
    try {
      path = SYSCALLS.getStr(path);
      var nofollow = 256 & flags, allowEmpty = 4096 & flags;
      return assert(!(flags &= -6401), `unknown flags in __syscall_newfstatat: ${flags}`), path = SYSCALLS.calculateAt(dirfd, path, allowEmpty), SYSCALLS.doStat(nofollow ? FS.lstat : FS.stat, path, buf);
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_openat: function(dirfd, path, flags, varargs) {
    SYSCALLS.varargs = varargs;
    try {
      path = SYSCALLS.getStr(path), path = SYSCALLS.calculateAt(dirfd, path);
      var mode = varargs ? function() {
        assert(null != SYSCALLS.varargs);
        var ret = HEAP32[+SYSCALLS.varargs >> 2];
        return SYSCALLS.varargs += 4, ret;
      }() : 0;
      return FS.open(path, flags, mode).fd;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_poll: function(fds, nfds, timeout) {
    try {
      for (var nonzero = 0, i = 0; i < nfds; i++) {
        var pollfd = fds + 8 * i, fd = HEAP32[pollfd >> 2], events = HEAP16[pollfd + 4 >> 1], mask = 32, stream = FS.getStream(fd);
        stream && (mask = SYSCALLS.DEFAULT_POLLMASK, stream.stream_ops.poll && (mask = stream.stream_ops.poll(stream, -1))), (mask &= 24 | events) && nonzero++, HEAP16[pollfd + 6 >> 1] = mask;
      }
      return nonzero;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_renameat: function(olddirfd, oldpath, newdirfd, newpath) {
    try {
      return oldpath = SYSCALLS.getStr(oldpath), newpath = SYSCALLS.getStr(newpath), oldpath = SYSCALLS.calculateAt(olddirfd, oldpath), newpath = SYSCALLS.calculateAt(newdirfd, newpath), FS.rename(oldpath, newpath), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_rmdir: function(path) {
    try {
      return path = SYSCALLS.getStr(path), FS.rmdir(path), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_stat64: function(path, buf) {
    try {
      return path = SYSCALLS.getStr(path), SYSCALLS.doStat(FS.stat, path, buf);
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_statfs64: function(path, size, buf) {
    try {
      return path = SYSCALLS.getStr(path), assert(64 === size), HEAP32[buf + 4 >> 2] = 4096, HEAP32[buf + 40 >> 2] = 4096, HEAP32[buf + 8 >> 2] = 1e6, HEAP32[buf + 12 >> 2] = 5e5, HEAP32[buf + 16 >> 2] = 5e5, HEAP32[buf + 20 >> 2] = FS.nextInode, HEAP32[buf + 24 >> 2] = 1e6, HEAP32[buf + 28 >> 2] = 42, HEAP32[buf + 44 >> 2] = 2, HEAP32[buf + 36 >> 2] = 255, 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, __syscall_unlinkat: function(dirfd, path, flags) {
    try {
      return path = SYSCALLS.getStr(path), path = SYSCALLS.calculateAt(dirfd, path), 0 === flags ? FS.unlink(path) : 512 === flags ? FS.rmdir(path) : abort("Invalid flags passed to unlinkat"), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return -e.errno;
    }
  }, _emscripten_memcpy_js: (dest, src, num) => HEAPU8.copyWithin(dest, src, src + num), _emscripten_throw_longjmp: () => {
    throw 1 / 0;
  }, call0: function(f_ref, out2) {
    proxy_convert_js_to_mp_obj_jsside((0, proxy_js_ref[f_ref])(), out2);
  }, call0_kwarg: function(f_ref, n_kw, key, value, out2) {
    const f = proxy_js_ref[f_ref], a = {};
    for (let i = 0; i < n_kw; ++i) {
      const k = UTF8ToString(getValue(key + 4 * i, "i32")), v = proxy_convert_mp_to_js_obj_jsside(value + 3 * i * 4);
      a[k] = v;
    }
    proxy_convert_js_to_mp_obj_jsside(f(a), out2);
  }, call1: function(f_ref, a0, out2) {
    const a0_js = proxy_convert_mp_to_js_obj_jsside(a0);
    proxy_convert_js_to_mp_obj_jsside((0, proxy_js_ref[f_ref])(a0_js), out2);
  }, call1_kwarg: function(f_ref, arg0, n_kw, key, value, out2) {
    const f = proxy_js_ref[f_ref], a0 = proxy_convert_mp_to_js_obj_jsside(arg0), a = {};
    for (let i = 0; i < n_kw; ++i) {
      const k = UTF8ToString(getValue(key + 4 * i, "i32")), v = proxy_convert_mp_to_js_obj_jsside(value + 3 * i * 4);
      a[k] = v;
    }
    proxy_convert_js_to_mp_obj_jsside(f(a0, a), out2);
  }, call2: function(f_ref, a0, a1, out2) {
    const a0_js = proxy_convert_mp_to_js_obj_jsside(a0), a1_js = proxy_convert_mp_to_js_obj_jsside(a1);
    proxy_convert_js_to_mp_obj_jsside((0, proxy_js_ref[f_ref])(a0_js, a1_js), out2);
  }, calln: function(f_ref, n_args, value, out2) {
    const f = proxy_js_ref[f_ref], a = [];
    for (let i = 0; i < n_args; ++i) {
      const v = proxy_convert_mp_to_js_obj_jsside(value + 3 * i * 4);
      a.push(v);
    }
    proxy_convert_js_to_mp_obj_jsside(f(...a), out2);
  }, create_promise: function(out_set, out_promise) {
    const out_set_js = proxy_convert_mp_to_js_obj_jsside(out_set);
    proxy_convert_js_to_mp_obj_jsside(new Promise(out_set_js), out_promise);
  }, emscripten_resize_heap: (requestedSize) => {
    var size, alignment, oldSize = HEAPU8.length;
    if (assert((requestedSize >>>= 0) > oldSize), requestedSize > 2147483648) return err(`Cannot enlarge memory, requested ${requestedSize} bytes, but the limit is 2147483648 bytes!`), false;
    for (var cutDown = 1; cutDown <= 4; cutDown *= 2) {
      var overGrownHeapSize = oldSize * (1 + 0.2 / cutDown);
      overGrownHeapSize = Math.min(overGrownHeapSize, requestedSize + 100663296);
      var newSize = Math.min(2147483648, (size = Math.max(requestedSize, overGrownHeapSize), assert(alignment = 65536, "alignment argument is required"), Math.ceil(size / alignment) * alignment));
      if (growMemory(newSize)) return true;
    }
    return err(`Failed to grow the heap from ${oldSize} bytes to ${newSize} bytes, not enough memory!`), false;
  }, fd_close: function(fd) {
    try {
      var stream = SYSCALLS.getStreamFromFD(fd);
      return FS.close(stream), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return e.errno;
    }
  }, fd_read: function(fd, iov, iovcnt, pnum) {
    try {
      var num = ((stream, iov2, iovcnt2, offset) => {
        for (var ret = 0, i = 0; i < iovcnt2; i++) {
          var ptr = HEAPU32[iov2 >> 2], len = HEAPU32[iov2 + 4 >> 2];
          iov2 += 8;
          var curr = FS.read(stream, HEAP8, ptr, len, offset);
          if (curr < 0) return -1;
          if (ret += curr, curr < len) break;
          void 0 !== offset && (offset += curr);
        }
        return ret;
      })(SYSCALLS.getStreamFromFD(fd), iov, iovcnt);
      return HEAPU32[pnum >> 2] = num, 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return e.errno;
    }
  }, fd_seek: function(fd, offset_low, offset_high, whence, newOffset) {
    var lo, hi, offset = (hi = offset_high, assert((lo = offset_low) == lo >>> 0 || lo == (0 | lo)), assert(hi === (0 | hi)), hi + 2097152 >>> 0 < 4194305 - !!lo ? (lo >>> 0) + 4294967296 * hi : NaN);
    try {
      if (isNaN(offset)) return 61;
      var stream = SYSCALLS.getStreamFromFD(fd);
      return FS.llseek(stream, offset, whence), tempI64 = [stream.position >>> 0, (tempDouble = stream.position, +Math.abs(tempDouble) >= 1 ? tempDouble > 0 ? +Math.floor(tempDouble / 4294967296) >>> 0 : ~~+Math.ceil((tempDouble - +(~~tempDouble >>> 0)) / 4294967296) >>> 0 : 0)], HEAP32[newOffset >> 2] = tempI64[0], HEAP32[newOffset + 4 >> 2] = tempI64[1], stream.getdents && 0 === offset && 0 === whence && (stream.getdents = null), 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return e.errno;
    }
  }, fd_sync: function(fd) {
    try {
      var stream = SYSCALLS.getStreamFromFD(fd);
      return stream.stream_ops?.fsync ? stream.stream_ops.fsync(stream) : 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return e.errno;
    }
  }, fd_write: function(fd, iov, iovcnt, pnum) {
    try {
      var num = ((stream, iov2, iovcnt2, offset) => {
        for (var ret = 0, i = 0; i < iovcnt2; i++) {
          var ptr = HEAPU32[iov2 >> 2], len = HEAPU32[iov2 + 4 >> 2];
          iov2 += 8;
          var curr = FS.write(stream, HEAP8, ptr, len, offset);
          if (curr < 0) return -1;
          if (ret += curr, curr < len) break;
          void 0 !== offset && (offset += curr);
        }
        return ret;
      })(SYSCALLS.getStreamFromFD(fd), iov, iovcnt);
      return HEAPU32[pnum >> 2] = num, 0;
    } catch (e) {
      if (void 0 === FS || "ErrnoError" !== e.name) throw e;
      return e.errno;
    }
  }, has_attr: function(jsref, str) {
    const base = proxy_js_ref[jsref];
    return UTF8ToString(str) in base;
  }, invoke_i: function(index) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)();
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_ii: function(index, a1) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)(a1);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_iii: function(index, a1, a2) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)(a1, a2);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_iiii: function(index, a1, a2, a3) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)(a1, a2, a3);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_iiiii: function(index, a1, a2, a3, a4) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)(a1, a2, a3, a4);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_iiiiii: function(index, a1, a2, a3, a4, a5) {
    var sp = stackSave();
    try {
      return getWasmTableEntry(index)(a1, a2, a3, a4, a5);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_v: function(index) {
    var sp = stackSave();
    try {
      getWasmTableEntry(index)();
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_vi: function(index, a1) {
    var sp = stackSave();
    try {
      getWasmTableEntry(index)(a1);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_vii: function(index, a1, a2) {
    var sp = stackSave();
    try {
      getWasmTableEntry(index)(a1, a2);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_viii: function(index, a1, a2, a3) {
    var sp = stackSave();
    try {
      getWasmTableEntry(index)(a1, a2, a3);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, invoke_viiii: function(index, a1, a2, a3, a4) {
    var sp = stackSave();
    try {
      getWasmTableEntry(index)(a1, a2, a3, a4);
    } catch (e) {
      if (stackRestore(sp), e !== e + 0) throw e;
      _setThrew(1, 0);
    }
  }, js_check_existing: function(c_ref) {
    return function(c_ref2) {
      const existing_obj = globalThis.proxy_js_map.get(c_ref2)?.deref();
      if (void 0 === existing_obj) return -1;
      for (let i = 0; i < globalThis.proxy_js_existing.length; ++i) if (void 0 === globalThis.proxy_js_existing[i]) return globalThis.proxy_js_existing[i] = existing_obj, i;
      return globalThis.proxy_js_existing.push(existing_obj), globalThis.proxy_js_existing.length - 1;
    }(c_ref);
  }, js_get_error_info: function(jsref, out_name, out_message) {
    const error = proxy_js_ref[jsref];
    proxy_convert_js_to_mp_obj_jsside(error.name, out_name), proxy_convert_js_to_mp_obj_jsside(error.message, out_message);
  }, js_get_iter: function(f_ref, out2) {
    proxy_convert_js_to_mp_obj_jsside(proxy_js_ref[f_ref][Symbol.iterator](), out2);
  }, js_get_proxy_js_ref_info: function(out2) {
    let used = 0;
    for (const elem of proxy_js_ref) void 0 !== elem && ++used;
    Module2.setValue(out2, proxy_js_ref.length, "i32"), Module2.setValue(out2 + 4, used, "i32");
  }, js_iter_next: function(f_ref, out2) {
    const ret = proxy_js_ref[f_ref].next();
    return !ret.done && (proxy_convert_js_to_mp_obj_jsside(ret.value, out2), true);
  }, js_reflect_construct: function(f_ref, n_args, args, out2) {
    const f = proxy_js_ref[f_ref], as = [];
    for (let i = 0; i < n_args; ++i) as.push(proxy_convert_mp_to_js_obj_jsside(args + 3 * i * 4));
    proxy_convert_js_to_mp_obj_jsside(Reflect.construct(f, as), out2);
  }, js_subscr_load: function(f_ref, index_ref, out2) {
    const target = proxy_js_ref[f_ref], index = function(target2, index_in) {
      let index2 = index_in;
      if ("number" == typeof index2 && (index2 < 0 && (index2 += target2.length), index2 < 0 || index2 >= target2.length)) throw new PythonError("IndexError", "index out of range");
      return index2;
    }(target, proxy_convert_mp_to_js_obj_jsside(index_ref));
    proxy_convert_js_to_mp_obj_jsside(target[index], out2);
  }, js_subscr_store: function(f_ref, idx, value) {
    proxy_js_ref[f_ref][proxy_convert_mp_to_js_obj_jsside(idx)] = proxy_convert_mp_to_js_obj_jsside(value);
  }, js_then_continue: function(jsref, py_resume, resolve, reject, out2) {
    const py_resume_js = proxy_convert_mp_to_js_obj_jsside(py_resume), resolve_js = proxy_convert_mp_to_js_obj_jsside(resolve), reject_js = proxy_convert_mp_to_js_obj_jsside(reject);
    proxy_convert_js_to_mp_obj_jsside(proxy_js_ref[jsref].then((result) => {
      py_resume_js(result, null, resolve_js, reject_js);
    }, (reason) => {
      py_resume_js(null, reason, resolve_js, reject_js);
    }), out2);
  }, js_then_reject: function(ret_value, reject) {
    let ret_value_js;
    try {
      ret_value_js = proxy_convert_mp_to_js_obj_jsside(ret_value);
    } catch (error) {
      ret_value_js = error;
    }
    proxy_convert_mp_to_js_obj_jsside(reject)(ret_value_js);
  }, js_then_resolve: function(ret_value, resolve) {
    const ret_value_js = proxy_convert_mp_to_js_obj_jsside(ret_value);
    proxy_convert_mp_to_js_obj_jsside(resolve)(ret_value_js);
  }, lookup_attr: function(jsref, str, out2) {
    const base = proxy_js_ref[jsref], attr = UTF8ToString(str);
    let value = base[attr];
    return (void 0 !== value || attr in base) && ("function" == typeof value && base !== globalThis && ("_ref" in value || (value = value.bind(base))), proxy_convert_js_to_mp_obj_jsside(value, out2), true);
  }, mp_js_random_u32: () => globalThis.crypto.getRandomValues(new Uint32Array(1))[0], mp_js_ticks_ms: () => Date.now() - MP_JS_EPOCH, mp_js_time_ms: () => Date.now(), proxy_convert_mp_to_js_then_js_to_js_then_js_to_mp_obj_jsside: function(out2) {
    const ret = proxy_convert_mp_to_js_obj_jsside(out2);
    proxy_convert_js_to_mp_obj_jsside(PyProxy.toJs(ret), out2);
  }, proxy_convert_mp_to_js_then_js_to_mp_obj_jsside: function(out2) {
    proxy_convert_js_to_mp_obj_jsside_force_double_proxy(proxy_convert_mp_to_js_obj_jsside(out2), out2);
  }, proxy_js_free_obj: function(js_ref) {
    js_ref >= PROXY_JS_REF_NUM_STATIC && (proxy_js_ref[js_ref] = void 0, js_ref < proxy_js_ref_next && (proxy_js_ref_next = js_ref));
  }, store_attr: function(jsref, attr_ptr, value_ref) {
    const attr = UTF8ToString(attr_ptr), value = proxy_convert_mp_to_js_obj_jsside(value_ref);
    proxy_js_ref[jsref][attr] = value;
  } }, wasmExports = function() {
    var info = { env: wasmImports, wasi_snapshot_preview1: wasmImports };
    function receiveInstance(instance, module) {
      var cb;
      return wasmExports = instance.exports, assert(wasmMemory = wasmExports.memory, "memory not found in wasm exports"), updateMemoryViews(), assert(wasmTable = wasmExports.__indirect_function_table, "table not found in wasm exports"), cb = wasmExports.__wasm_call_ctors, __ATINIT__.unshift(cb), removeRunDependency("wasm-instantiate"), wasmExports;
    }
    addRunDependency("wasm-instantiate");
    var binary, binaryFile, imports, callback, trueModule = Module2;
    if (Module2.instantiateWasm) try {
      return Module2.instantiateWasm(info, receiveInstance);
    } catch (e) {
      err(`Module.instantiateWasm callback failed with error: ${e}`), readyPromiseReject(e);
    }
    return wasmBinaryFile || (wasmBinaryFile = findWasmBinary()), (binary = wasmBinary, binaryFile = wasmBinaryFile, imports = info, callback = function(result) {
      assert(Module2 === trueModule, "the Module object should not be replaced during async compilation - perhaps the order of HTML elements is wrong?"), trueModule = null, receiveInstance(result.instance);
    }, binary || "function" != typeof WebAssembly.instantiateStreaming || isDataURI(binaryFile) || isFileURI(binaryFile) || ENVIRONMENT_IS_NODE || "function" != typeof fetch ? instantiateArrayBuffer(binaryFile, imports, callback) : fetch(binaryFile, { credentials: "same-origin" }).then((response) => WebAssembly.instantiateStreaming(response, imports).then(callback, function(reason) {
      return err(`wasm streaming compile failed: ${reason}`), err("falling back to ArrayBuffer instantiation"), instantiateArrayBuffer(binaryFile, imports, callback);
    }))).catch(readyPromiseReject), {};
  }(), _fflush = (createExportWrapper("__wasm_call_ctors", 0), Module2._free = createExportWrapper("free", 1), Module2._malloc = createExportWrapper("malloc", 1), Module2._mp_sched_keyboard_interrupt = createExportWrapper("mp_sched_keyboard_interrupt", 0), Module2._mp_js_init = createExportWrapper("mp_js_init", 2), Module2._mp_js_register_js_module = createExportWrapper("mp_js_register_js_module", 2), Module2._mp_js_do_import = createExportWrapper("mp_js_do_import", 2), Module2._proxy_convert_mp_to_js_obj_cside = createExportWrapper("proxy_convert_mp_to_js_obj_cside", 2), Module2._mp_js_do_exec = createExportWrapper("mp_js_do_exec", 3), Module2._mp_js_do_exec_async = createExportWrapper("mp_js_do_exec_async", 3), Module2._mp_js_repl_init = createExportWrapper("mp_js_repl_init", 0), Module2._mp_js_repl_process_char = createExportWrapper("mp_js_repl_process_char", 1), Module2._mp_hal_get_interrupt_char = createExportWrapper("mp_hal_get_interrupt_char", 0), Module2._proxy_c_init = createExportWrapper("proxy_c_init", 0), Module2._proxy_c_free_obj = createExportWrapper("proxy_c_free_obj", 1), Module2._proxy_c_to_js_call = createExportWrapper("proxy_c_to_js_call", 4), Module2._proxy_c_to_js_dir = createExportWrapper("proxy_c_to_js_dir", 2), Module2._proxy_c_to_js_has_attr = createExportWrapper("proxy_c_to_js_has_attr", 2), Module2._proxy_c_to_js_lookup_attr = createExportWrapper("proxy_c_to_js_lookup_attr", 3), Module2._proxy_c_to_js_store_attr = createExportWrapper("proxy_c_to_js_store_attr", 3), Module2._proxy_c_to_js_delete_attr = createExportWrapper("proxy_c_to_js_delete_attr", 2), Module2._proxy_c_to_js_get_type = createExportWrapper("proxy_c_to_js_get_type", 1), Module2._proxy_c_to_js_get_array = createExportWrapper("proxy_c_to_js_get_array", 2), Module2._proxy_c_to_js_get_dict = createExportWrapper("proxy_c_to_js_get_dict", 2), Module2._proxy_c_to_js_get_iter = createExportWrapper("proxy_c_to_js_get_iter", 1), Module2._proxy_c_to_js_iternext = createExportWrapper("proxy_c_to_js_iternext", 2), Module2._proxy_c_to_js_resume = createExportWrapper("proxy_c_to_js_resume", 2), createExportWrapper("fflush", 1)), _strerror = createExportWrapper("strerror", 1), _setThrew = createExportWrapper("setThrew", 2), _emscripten_stack_init = () => (_emscripten_stack_init = wasmExports.emscripten_stack_init)(), _emscripten_stack_get_end = () => (_emscripten_stack_get_end = wasmExports.emscripten_stack_get_end)(), __emscripten_stack_restore = (a0) => (__emscripten_stack_restore = wasmExports._emscripten_stack_restore)(a0), __emscripten_stack_alloc = (a0) => (__emscripten_stack_alloc = wasmExports._emscripten_stack_alloc)(a0), _emscripten_stack_get_current = () => (_emscripten_stack_get_current = wasmExports.emscripten_stack_get_current)();
  function stackCheckInit() {
    var max;
    _emscripten_stack_init(), assert(!(3 & (max = _emscripten_stack_get_end()))), 0 == max && (max += 4), HEAPU32[max >> 2] = 34821223, HEAPU32[max + 4 >> 2] = 2310721022, HEAPU32[0] = 1668509029;
  }
  function run() {
    function doRun() {
      calledRun || (calledRun = true, Module2.calledRun = true, ABORT || (assert(!runtimeInitialized), runtimeInitialized = true, checkStackCookie(), Module2.noFSInit || FS.initialized || FS.init(), FS.ignorePermissions = false, TTY.init(), callRuntimeCallbacks(__ATINIT__), readyPromiseResolve(Module2), Module2.onRuntimeInitialized?.(), assert(!Module2._main, 'compiled without a main, but one is present. if you added it from JS, use Module["onRuntimeInitialized"]'), function() {
        if (checkStackCookie(), Module2.postRun) for ("function" == typeof Module2.postRun && (Module2.postRun = [Module2.postRun]); Module2.postRun.length; ) cb = Module2.postRun.shift(), __ATPOSTRUN__.unshift(cb);
        var cb;
        callRuntimeCallbacks(__ATPOSTRUN__);
      }()));
    }
    runDependencies > 0 || (stackCheckInit(), function() {
      if (Module2.preRun) for ("function" == typeof Module2.preRun && (Module2.preRun = [Module2.preRun]); Module2.preRun.length; ) cb = Module2.preRun.shift(), __ATPRERUN__.unshift(cb);
      var cb;
      callRuntimeCallbacks(__ATPRERUN__);
    }(), runDependencies > 0 || (Module2.setStatus ? (Module2.setStatus("Running..."), setTimeout(() => {
      setTimeout(() => Module2.setStatus(""), 1), doRun();
    }, 1)) : doRun(), checkStackCookie()));
  }
  if (Module2.ccall = ccall, Module2.cwrap = (ident, returnType, argTypes, opts) => (...args) => ccall(ident, returnType, argTypes, args), Module2.setValue = function(ptr, value, type = "i8") {
    switch (type.endsWith("*") && (type = "*"), type) {
      case "i1":
      case "i8":
        HEAP8[ptr] = value;
        break;
      case "i16":
        HEAP16[ptr >> 1] = value;
        break;
      case "i32":
        HEAP32[ptr >> 2] = value;
        break;
      case "i64":
        abort("to do setValue(i64) use WASM_BIGINT");
      case "float":
        HEAPF32[ptr >> 2] = value;
        break;
      case "double":
        HEAPF64[ptr >> 3] = value;
        break;
      case "*":
        HEAPU32[ptr >> 2] = value;
        break;
      default:
        abort(`invalid type for setValue: ${type}`);
    }
  }, Module2.getValue = getValue, Module2.PATH = PATH, Module2.PATH_FS = PATH_FS, Module2.UTF8ToString = UTF8ToString, Module2.stringToUTF8 = stringToUTF8, Module2.lengthBytesUTF8 = lengthBytesUTF8, Module2.FS = FS, ["writeI53ToI64", "writeI53ToI64Clamped", "writeI53ToI64Signaling", "writeI53ToU64Clamped", "writeI53ToU64Signaling", "readI53FromI64", "readI53FromU64", "convertI32PairToI53", "convertU32PairToI53", "getTempRet0", "setTempRet0", "exitJS", "inetPton4", "inetNtop4", "inetPton6", "inetNtop6", "readSockaddr", "writeSockaddr", "emscriptenLog", "readEmAsmArgs", "jstoi_q", "getExecutableName", "listenOnce", "autoResumeAudioContext", "dynCallLegacy", "getDynCaller", "dynCall", "handleException", "keepRuntimeAlive", "runtimeKeepalivePush", "runtimeKeepalivePop", "callUserCallback", "maybeExit", "asmjsMangle", "HandleAllocator", "getNativeTypeSize", "STACK_SIZE", "STACK_ALIGN", "POINTER_SIZE", "ASSERTIONS", "uleb128Encode", "sigToWasmTypes", "generateFuncType", "convertJsFunctionToWasm", "getEmptyTableSlot", "updateTableMap", "getFunctionAddress", "addFunction", "removeFunction", "reallyNegative", "unSign", "strLen", "reSign", "formatString", "intArrayToString", "AsciiToString", "stringToAscii", "UTF16ToString", "stringToUTF16", "lengthBytesUTF16", "UTF32ToString", "stringToUTF32", "lengthBytesUTF32", "stringToNewUTF8", "registerKeyEventCallback", "maybeCStringToJsString", "findEventTarget", "getBoundingClientRect", "fillMouseEventData", "registerMouseEventCallback", "registerWheelEventCallback", "registerUiEventCallback", "registerFocusEventCallback", "fillDeviceOrientationEventData", "registerDeviceOrientationEventCallback", "fillDeviceMotionEventData", "registerDeviceMotionEventCallback", "screenOrientation", "fillOrientationChangeEventData", "registerOrientationChangeEventCallback", "fillFullscreenChangeEventData", "registerFullscreenChangeEventCallback", "JSEvents_requestFullscreen", "JSEvents_resizeCanvasForFullscreen", "registerRestoreOldStyle", "hideEverythingExceptGivenElement", "restoreHiddenElements", "setLetterbox", "softFullscreenResizeWebGLRenderTarget", "doRequestFullscreen", "fillPointerlockChangeEventData", "registerPointerlockChangeEventCallback", "registerPointerlockErrorEventCallback", "requestPointerLock", "fillVisibilityChangeEventData", "registerVisibilityChangeEventCallback", "registerTouchEventCallback", "fillGamepadEventData", "registerGamepadEventCallback", "registerBeforeUnloadEventCallback", "fillBatteryEventData", "battery", "registerBatteryEventCallback", "setCanvasElementSize", "getCanvasElementSize", "jsStackTrace", "getCallstack", "convertPCtoSourceLocation", "getEnvStrings", "checkWasiClock", "wasiRightsToMuslOFlags", "wasiOFlagsToMuslOFlags", "createDyncallWrapper", "safeSetTimeout", "setImmediateWrapped", "clearImmediateWrapped", "polyfillSetImmediate", "getPromise", "makePromise", "idsToPromises", "makePromiseCallback", "ExceptionInfo", "findMatchingCatch", "Browser_asyncPrepareDataCounter", "setMainLoop", "isLeapYear", "ydayFromDate", "arraySum", "addDays", "getSocketFromFD", "getSocketAddress", "FS_unlink", "FS_mkdirTree", "_setNetworkCallback", "heapObjectForWebGLType", "toTypedArrayIndex", "webgl_enable_ANGLE_instanced_arrays", "webgl_enable_OES_vertex_array_object", "webgl_enable_WEBGL_draw_buffers", "webgl_enable_WEBGL_multi_draw", "webgl_enable_EXT_polygon_offset_clamp", "webgl_enable_EXT_clip_control", "webgl_enable_WEBGL_polygon_mode", "emscriptenWebGLGet", "computeUnpackAlignedImageSize", "colorChannelsInGlTextureFormat", "emscriptenWebGLGetTexPixelData", "emscriptenWebGLGetUniform", "webglGetUniformLocation", "webglPrepareUniformLocationsBeforeFirstUse", "webglGetLeftBracePos", "emscriptenWebGLGetVertexAttrib", "__glGetActiveAttribOrUniform", "writeGLArray", "registerWebGlEventCallback", "runAndAbortIfError", "ALLOC_NORMAL", "ALLOC_STACK", "allocate", "writeStringToMemory", "writeAsciiToMemory", "setErrNo", "demangle", "stackTrace"].forEach(function(sym) {
    "undefined" == typeof globalThis || Object.getOwnPropertyDescriptor(globalThis, sym) || Object.defineProperty(globalThis, sym, { configurable: true, get() {
      var msg = `\`${sym}\` is a library symbol and not included by default; add it to your library.js __deps or to DEFAULT_LIBRARY_FUNCS_TO_INCLUDE on the command line`, librarySymbol = sym;
      librarySymbol.startsWith("_") || (librarySymbol = "$" + sym), msg += ` (e.g. -sDEFAULT_LIBRARY_FUNCS_TO_INCLUDE='${librarySymbol}')`, isExportedByForceFilesystem(sym) && (msg += ". Alternatively, forcing filesystem support (-sFORCE_FILESYSTEM) can export this for you"), warnOnce(msg);
    } }), unexportedRuntimeSymbol(sym);
  }), ["run", "addOnPreRun", "addOnInit", "addOnPreMain", "addOnExit", "addOnPostRun", "addRunDependency", "removeRunDependency", "out", "err", "callMain", "abort", "wasmMemory", "wasmExports", "writeStackCookie", "checkStackCookie", "convertI32PairToI53Checked", "stackSave", "stackRestore", "stackAlloc", "ptrToString", "zeroMemory", "getHeapMax", "growMemory", "ENV", "ERRNO_CODES", "strError", "DNS", "Protocols", "Sockets", "initRandomFill", "randomFill", "timers", "warnOnce", "readEmAsmArgsArray", "jstoi_s", "asyncLoad", "alignMemory", "mmapAlloc", "wasmTable", "noExitRuntime", "getCFunc", "freeTableIndexes", "functionsInTableMap", "UTF8Decoder", "UTF8ArrayToString", "stringToUTF8Array", "intArrayFromString", "UTF16Decoder", "stringToUTF8OnStack", "writeArrayToMemory", "JSEvents", "specialHTMLTargets", "findCanvasEventTarget", "currentFullscreenStrategy", "restoreOldWindowedStyle", "UNWIND_CACHE", "ExitStatus", "doReadv", "doWritev", "promiseMap", "uncaughtExceptionCount", "exceptionLast", "exceptionCaught", "Browser", "getPreloadedImageData__data", "wget", "MONTH_DAYS_REGULAR", "MONTH_DAYS_LEAP", "MONTH_DAYS_REGULAR_CUMULATIVE", "MONTH_DAYS_LEAP_CUMULATIVE", "SYSCALLS", "preloadPlugins", "FS_createPreloadedFile", "FS_modeStringToFlags", "FS_getMode", "FS_stdin_getChar_buffer", "FS_stdin_getChar", "FS_createPath", "FS_createDevice", "FS_readFile", "FS_createDataFile", "FS_createLazyFile", "MEMFS", "TTY", "PIPEFS", "SOCKFS", "tempFixedLengthArray", "miniTempWebGLFloatBuffers", "miniTempWebGLIntBuffers", "GL", "AL", "GLUT", "EGL", "GLEW", "IDBStore", "SDL", "SDL_gfx", "allocateUTF8", "allocateUTF8OnStack", "print", "printErr"].forEach(unexportedRuntimeSymbol), dependenciesFulfilled = function runCaller() {
    calledRun || run(), calledRun || (dependenciesFulfilled = runCaller);
  }, Module2.preInit) for ("function" == typeof Module2.preInit && (Module2.preInit = [Module2.preInit]); Module2.preInit.length > 0; ) Module2.preInit.pop()();
  run(), moduleRtn = readyPromise;
  for (const prop2 of Object.keys(Module2)) prop2 in moduleArg || Object.defineProperty(moduleArg, prop2, { configurable: true, get() {
    abort(`Access to module property ('${prop2}') is no longer possible via the module constructor argument; Instead, use the result of the module constructor.`);
  } });
  return moduleRtn;
});
var micropython_default = _createMicroPythonModule;
async function loadMicroPython(options) {
  const { pystack, heapsize, url, stdin, stdout, stderr, linebuffer } = Object.assign({ pystack: 2048, heapsize: 1048576, linebuffer: true }, options);
  let Module2 = { locateFile: (path, scriptDirectory) => url || scriptDirectory + path };
  Module2._textDecoder = new TextDecoder(), void 0 !== stdin && (Module2.stdin = stdin), void 0 !== stdout && (linebuffer ? (Module2._stdoutBuffer = [], Module2.stdout = (c) => {
    10 === c ? (stdout(Module2._textDecoder.decode(new Uint8Array(Module2._stdoutBuffer))), Module2._stdoutBuffer = []) : Module2._stdoutBuffer.push(c);
  }) : Module2.stdout = (c) => stdout(new Uint8Array([c]))), void 0 !== stderr && (linebuffer ? (Module2._stderrBuffer = [], Module2.stderr = (c) => {
    10 === c ? (stderr(Module2._textDecoder.decode(new Uint8Array(Module2._stderrBuffer))), Module2._stderrBuffer = []) : Module2._stderrBuffer.push(c);
  }) : Module2.stderr = (c) => stderr(new Uint8Array([c]))), Module2 = await _createMicroPythonModule(Module2), globalThis.Module = Module2, proxy_js_init();
  const pyimport = (name) => {
    const value = Module2._malloc(12);
    return Module2.ccall("mp_js_do_import", "null", ["string", "pointer"], [name, value]), proxy_convert_mp_to_js_obj_jsside_with_free(value);
  };
  return Module2.ccall("mp_js_init", "null", ["number", "number"], [pystack, heapsize]), Module2.ccall("proxy_c_init", "null", [], []), { _module: Module2, PyProxy, FS: Module2.FS, globals: { __dict__: pyimport("__main__").__dict__, get(key) {
    return this.__dict__[key];
  }, set(key, value) {
    this.__dict__[key] = value;
  }, delete(key) {
    delete this.__dict__[key];
  } }, registerJsModule(name, module) {
    const value = Module2._malloc(12);
    proxy_convert_js_to_mp_obj_jsside(module, value), Module2.ccall("mp_js_register_js_module", "null", ["string", "pointer"], [name, value]), Module2._free(value);
  }, pyimport, runPython(code) {
    const len = Module2.lengthBytesUTF8(code), buf = Module2._malloc(len + 1);
    Module2.stringToUTF8(code, buf, len + 1);
    const value = Module2._malloc(12);
    return Module2.ccall("mp_js_do_exec", "number", ["pointer", "number", "pointer"], [buf, len, value]), Module2._free(buf), proxy_convert_mp_to_js_obj_jsside_with_free(value);
  }, runPythonAsync(code) {
    const len = Module2.lengthBytesUTF8(code), buf = Module2._malloc(len + 1);
    Module2.stringToUTF8(code, buf, len + 1);
    const value = Module2._malloc(12);
    Module2.ccall("mp_js_do_exec_async", "number", ["pointer", "number", "pointer"], [buf, len, value]), Module2._free(buf);
    const ret = proxy_convert_mp_to_js_obj_jsside_with_free(value);
    return ret instanceof PyProxyThenable ? Promise.resolve(ret) : ret;
  }, replInit() {
    Module2.ccall("mp_js_repl_init", "null", ["null"]);
  }, replProcessChar: (chr) => Module2.ccall("mp_js_repl_process_char", "number", ["number"], [chr]), replProcessCharWithAsyncify: async (chr) => Module2.ccall("mp_js_repl_process_char", "number", ["number"], [chr], { async: true }) };
}
if (globalThis.loadMicroPython = loadMicroPython, "object" == typeof process && "object" == typeof process.versions && "string" == typeof process.versions.node && process.argv.length > 1) {
  const path = await import("path"), url = await import("url"), pathToThisFile = path.resolve(url.fileURLToPath(import.meta.url)), pathPassedToNode = path.resolve(process.argv[1]);
  pathToThisFile.includes(pathPassedToNode) && async function() {
    const fs = await import("fs");
    let heap_size = 131072, contents = "", repl = true;
    for (let i = 2; i < process.argv.length; i++) if ("-X" === process.argv[i] && i < process.argv.length - 1) {
      if (process.argv[i + 1].includes("heapsize=")) {
        heap_size = parseInt(process.argv[i + 1].split("heapsize=")[1]);
        const suffix = process.argv[i + 1].substr(-1).toLowerCase();
        "k" === suffix ? heap_size *= 1024 : "m" === suffix && (heap_size *= 1048576), ++i;
      }
    } else contents += fs.readFileSync(process.argv[i], "utf8"), repl = false;
    false === process.stdin.isTTY && (contents = fs.readFileSync(0, "utf8"), repl = false);
    const mp = await loadMicroPython({ heapsize: heap_size, stdout: (data) => process.stdout.write(data), linebuffer: false });
    if (repl) mp.replInit(), process.stdin.setRawMode(true), process.stdin.on("data", (data) => {
      for (let i = 0; i < data.length; i++) mp.replProcessCharWithAsyncify(data[i]).then((result) => {
        result && process.exit();
      });
    });
    else {
      if (contents.endsWith("asyncio.run(main())\n")) {
        const asyncio = mp.pyimport("asyncio");
        asyncio.run = async (task) => {
          await asyncio.create_task(task);
        };
      }
      try {
        mp.runPython(contents);
      } catch (error) {
        if ("PythonError" !== error.name) throw error;
        "SystemExit" === error.type || console.error(error.message);
      }
    }
  }();
}
var PyProxy = class _PyProxy {
  constructor(ref) {
    this._ref = ref;
  }
  static toJs(js_obj) {
    if (!(js_obj instanceof _PyProxy)) return js_obj;
    const type = Module.ccall("proxy_c_to_js_get_type", "number", ["number"], [js_obj._ref]);
    if (1 === type || 2 === type) {
      const array_ref = Module._malloc(8), item = Module._malloc(12);
      Module.ccall("proxy_c_to_js_get_array", "null", ["number", "pointer"], [js_obj._ref, array_ref]);
      const len = Module.getValue(array_ref, "i32"), items_ptr = Module.getValue(array_ref + 4, "i32"), js_array = [];
      for (let i = 0; i < len; ++i) {
        Module.ccall("proxy_convert_mp_to_js_obj_cside", "null", ["pointer", "pointer"], [Module.getValue(items_ptr + 4 * i, "i32"), item]);
        const js_item = proxy_convert_mp_to_js_obj_jsside(item);
        js_array.push(_PyProxy.toJs(js_item));
      }
      return Module._free(array_ref), Module._free(item), js_array;
    }
    if (3 === type) {
      const map_ref = Module._malloc(8), item = Module._malloc(12);
      Module.ccall("proxy_c_to_js_get_dict", "null", ["number", "pointer"], [js_obj._ref, map_ref]);
      const alloc = Module.getValue(map_ref, "i32"), table_ptr = Module.getValue(map_ref + 4, "i32"), js_dict = {};
      for (let i = 0; i < alloc; ++i) {
        const mp_key = Module.getValue(table_ptr + 8 * i, "i32");
        if (mp_key > 8) {
          Module.ccall("proxy_convert_mp_to_js_obj_cside", "null", ["pointer", "pointer"], [mp_key, item]);
          const js_key = proxy_convert_mp_to_js_obj_jsside(item), mp_value = Module.getValue(table_ptr + 8 * i + 4, "i32");
          Module.ccall("proxy_convert_mp_to_js_obj_cside", "null", ["pointer", "pointer"], [mp_value, item]);
          const js_value = proxy_convert_mp_to_js_obj_jsside(item);
          js_dict[js_key] = _PyProxy.toJs(js_value);
        }
      }
      return Module._free(map_ref), Module._free(item), js_dict;
    }
    return js_obj;
  }
};
var py_proxy_handler = { isExtensible: () => true, ownKeys(target) {
  const value = Module._malloc(12);
  Module.ccall("proxy_c_to_js_dir", "null", ["number", "pointer"], [target._ref, value]);
  const dir = proxy_convert_mp_to_js_obj_jsside_with_free(value);
  return PyProxy.toJs(dir).filter((attr) => !attr.startsWith("__"));
}, getOwnPropertyDescriptor: (target, prop) => ({ value: target[prop], enumerable: true, writable: true, configurable: true }), has: (target, prop) => Module.ccall("proxy_c_to_js_has_attr", "number", ["number", "string"], [target._ref, prop]), get(target, prop) {
  if ("_ref" === prop) return target._ref;
  if ("then" === prop) return null;
  if (prop === Symbol.iterator) {
    const iter_ref = Module.ccall("proxy_c_to_js_get_iter", "number", ["number"], [target._ref]);
    return function* () {
      const value2 = Module._malloc(12);
      for (; ; ) {
        if (!Module.ccall("proxy_c_to_js_iternext", "number", ["number", "pointer"], [iter_ref, value2])) break;
        yield proxy_convert_mp_to_js_obj_jsside(value2);
      }
      Module._free(value2);
    };
  }
  const value = Module._malloc(12);
  return Module.ccall("proxy_c_to_js_lookup_attr", "null", ["number", "string", "pointer"], [target._ref, prop, value]), proxy_convert_mp_to_js_obj_jsside_with_free(value);
}, set(target, prop, value) {
  const value_conv = Module._malloc(12);
  proxy_convert_js_to_mp_obj_jsside(value, value_conv);
  const ret = Module.ccall("proxy_c_to_js_store_attr", "number", ["number", "string", "number"], [target._ref, prop, value_conv]);
  return Module._free(value_conv), ret;
}, deleteProperty: (target, prop) => Module.ccall("proxy_c_to_js_delete_attr", "number", ["number", "string"], [target._ref, prop]) };
var PyProxyThenable = class {
  constructor(ref) {
    this._ref = ref;
  }
  then(resolve, reject) {
    const values = Module._malloc(36);
    return proxy_convert_js_to_mp_obj_jsside(resolve, values + 12), proxy_convert_js_to_mp_obj_jsside(reject, values + 24), Module.ccall("proxy_c_to_js_resume", "null", ["number", "pointer"], [this._ref, values]), proxy_convert_mp_to_js_obj_jsside_with_free(values);
  }
};
var PROXY_JS_REF_NUM_STATIC = 2;
var PROXY_KIND_MP_EXCEPTION = -1;
var PROXY_KIND_MP_NULL = 0;
var PROXY_KIND_MP_NONE = 1;
var PROXY_KIND_MP_BOOL = 2;
var PROXY_KIND_MP_INT = 3;
var PROXY_KIND_MP_FLOAT = 4;
var PROXY_KIND_MP_STR = 5;
var PROXY_KIND_MP_CALLABLE = 6;
var PROXY_KIND_MP_GENERATOR = 7;
var PROXY_KIND_MP_JSPROXY = 9;
var PROXY_KIND_MP_EXISTING = 10;
var PROXY_KIND_JS_UNDEFINED = 0;
var PROXY_KIND_JS_NULL = 1;
var PROXY_KIND_JS_BOOLEAN = 2;
var PROXY_KIND_JS_INTEGER = 3;
var PROXY_KIND_JS_DOUBLE = 4;
var PROXY_KIND_JS_STRING = 5;
var PROXY_KIND_JS_OBJECT = 6;
var PROXY_KIND_JS_PYPROXY = 7;
var PythonError = class extends Error {
  constructor(exc_type, exc_details) {
    super(exc_details), this.name = "PythonError", this.type = exc_type;
  }
};
function proxy_js_init() {
  globalThis.proxy_js_ref = [globalThis, void 0], globalThis.proxy_js_ref_next = PROXY_JS_REF_NUM_STATIC, globalThis.proxy_js_map = /* @__PURE__ */ new Map(), globalThis.proxy_js_existing = [void 0], globalThis.pyProxyFinalizationRegistry = new FinalizationRegistry((cRef) => {
    globalThis.proxy_js_map.delete(cRef), Module.ccall("proxy_c_free_obj", "null", ["number"], [cRef]);
  });
}
function proxy_js_add_obj(js_obj) {
  for (; proxy_js_ref_next < proxy_js_ref.length; ) {
    if (void 0 === proxy_js_ref[proxy_js_ref_next]) {
      const id2 = proxy_js_ref_next;
      return ++proxy_js_ref_next, proxy_js_ref[id2] = js_obj, id2;
    }
    ++proxy_js_ref_next;
  }
  const id = proxy_js_ref.length;
  return proxy_js_ref[id] = js_obj, proxy_js_ref_next = proxy_js_ref.length, id;
}
function proxy_convert_js_to_mp_obj_jsside(js_obj, out) {
  let kind;
  if (void 0 === js_obj) kind = PROXY_KIND_JS_UNDEFINED;
  else if (null === js_obj) kind = PROXY_KIND_JS_NULL;
  else if ("boolean" == typeof js_obj) kind = PROXY_KIND_JS_BOOLEAN, Module.setValue(out + 4, js_obj, "i32");
  else if ("number" == typeof js_obj) if (Number.isInteger(js_obj)) kind = PROXY_KIND_JS_INTEGER, Module.setValue(out + 4, js_obj, "i32");
  else {
    kind = PROXY_KIND_JS_DOUBLE;
    const temp = out + 4 & -8;
    Module.setValue(temp, js_obj, "double");
    const double_lo = Module.getValue(temp, "i32"), double_hi = Module.getValue(temp + 4, "i32");
    Module.setValue(out + 4, double_lo, "i32"), Module.setValue(out + 8, double_hi, "i32");
  }
  else if ("string" == typeof js_obj) {
    kind = PROXY_KIND_JS_STRING;
    const len = Module.lengthBytesUTF8(js_obj), buf = Module._malloc(len + 1);
    Module.stringToUTF8(js_obj, buf, len + 1), Module.setValue(out + 4, len, "i32"), Module.setValue(out + 8, buf, "i32");
  } else if (js_obj instanceof PyProxy || "function" == typeof js_obj && "_ref" in js_obj || js_obj instanceof PyProxyThenable) kind = PROXY_KIND_JS_PYPROXY, Module.setValue(out + 4, js_obj._ref, "i32");
  else {
    kind = PROXY_KIND_JS_OBJECT;
    const id = proxy_js_add_obj(js_obj);
    Module.setValue(out + 4, id, "i32");
  }
  Module.setValue(out + 0, kind, "i32");
}
function proxy_convert_js_to_mp_obj_jsside_force_double_proxy(js_obj, out) {
  if (js_obj instanceof PyProxy || "function" == typeof js_obj && "_ref" in js_obj || js_obj instanceof PyProxyThenable) {
    const kind = PROXY_KIND_JS_OBJECT, id = proxy_js_add_obj(js_obj);
    Module.setValue(out + 4, id, "i32"), Module.setValue(out + 0, kind, "i32");
  } else proxy_convert_js_to_mp_obj_jsside(js_obj, out);
}
function proxy_convert_mp_to_js_obj_jsside(value) {
  const kind = Module.getValue(value, "i32");
  let obj;
  if (kind === PROXY_KIND_MP_EXCEPTION) {
    const str_len = Module.getValue(value + 4, "i32"), str_ptr = Module.getValue(value + 8, "i32"), str = Module.UTF8ToString(str_ptr, str_len);
    Module._free(str_ptr);
    const str_split = str.split("");
    throw new PythonError(str_split[0], str_split[1]);
  }
  if (kind === PROXY_KIND_MP_NULL) throw new Error("NULL object");
  if (kind === PROXY_KIND_MP_NONE) obj = null;
  else if (kind === PROXY_KIND_MP_BOOL) obj = !!Module.getValue(value + 4, "i32");
  else if (kind === PROXY_KIND_MP_INT) obj = Module.getValue(value + 4, "i32");
  else if (kind === PROXY_KIND_MP_FLOAT) {
    const temp = value + 4 & -8, double_lo = Module.getValue(value + 4, "i32"), double_hi = Module.getValue(value + 8, "i32");
    Module.setValue(temp, double_lo, "i32"), Module.setValue(temp + 4, double_hi, "i32"), obj = Module.getValue(temp, "double");
  } else if (kind === PROXY_KIND_MP_STR) {
    const str_len = Module.getValue(value + 4, "i32"), str_ptr = Module.getValue(value + 8, "i32");
    obj = Module.UTF8ToString(str_ptr, str_len);
  } else if (kind === PROXY_KIND_MP_JSPROXY) {
    const id = Module.getValue(value + 4, "i32");
    obj = proxy_js_ref[id];
  } else if (kind === PROXY_KIND_MP_EXISTING) {
    const id = Module.getValue(value + 4, "i32");
    obj = globalThis.proxy_js_existing[id], globalThis.proxy_js_existing[id] = void 0;
  } else {
    const id = Module.getValue(value + 4, "i32");
    if (kind === PROXY_KIND_MP_CALLABLE) obj = (...args) => function(target, argumentsList) {
      let args2 = 0;
      for (; argumentsList.length > 0 && void 0 === argumentsList[argumentsList.length - 1]; ) argumentsList.pop();
      if (argumentsList.length > 0) {
        args2 = Module._malloc(3 * argumentsList.length * 4);
        for (const i in argumentsList) proxy_convert_js_to_mp_obj_jsside(argumentsList[i], args2 + 3 * i * 4);
      }
      const value2 = Module._malloc(12);
      Module.ccall("proxy_c_to_js_call", "null", ["number", "number", "number", "pointer"], [target, argumentsList.length, args2, value2]), argumentsList.length > 0 && Module._free(args2);
      const ret = proxy_convert_mp_to_js_obj_jsside_with_free(value2);
      return ret instanceof PyProxyThenable ? Promise.resolve(ret) : ret;
    }(id, args), obj._ref = id;
    else if (kind === PROXY_KIND_MP_GENERATOR) obj = new PyProxyThenable(id);
    else {
      const target = new PyProxy(id);
      obj = new Proxy(target, py_proxy_handler);
    }
    globalThis.pyProxyFinalizationRegistry.register(obj, id), globalThis.proxy_js_map.set(id, new WeakRef(obj));
  }
  return obj;
}
function proxy_convert_mp_to_js_obj_jsside_with_free(value) {
  const ret = proxy_convert_mp_to_js_obj_jsside(value);
  return Module._free(value), ret;
}
export {
  micropython_default as default,
  loadMicroPython
};
