/*
	Eventually by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function() {

	"use strict";

	var	$body = document.querySelector('body');

	
	// Methods/polyfills.

		// classList | (c) @remy | github.com/remy/polyfills | rem.mit-license.org
			!function(){function t(t){this.el=t;for(var n=t.className.replace(/^\s+|\s+$/g,"").split(/\s+/),i=0;i<n.length;i++)e.call(this,n[i])}function n(t,n,i){Object.defineProperty?Object.defineProperty(t,n,{get:i}):t.__defineGetter__(n,i)}if(!("undefined"==typeof window.Element||"classList"in document.documentElement)){var i=Array.prototype,e=i.push,s=i.splice,o=i.join;t.prototype={add:function(t){this.contains(t)||(e.call(this,t),this.el.className=this.toString())},contains:function(t){return-1!=this.el.className.indexOf(t)},item:function(t){return this[t]||null},remove:function(t){if(this.contains(t)){for(var n=0;n<this.length&&this[n]!=t;n++);s.call(this,n,1),this.el.className=this.toString()}},toString:function(){return o.call(this," ")},toggle:function(t){return this.contains(t)?this.remove(t):this.add(t),this.contains(t)}},window.DOMTokenList=t,n(Element.prototype,"classList",function(){return new t(this)})}}();

		// canUse
			window.canUse=function(p){if(!window._canUse)window._canUse=document.createElement("div");var e=window._canUse.style,up=p.charAt(0).toUpperCase()+p.slice(1);return p in e||"Moz"+up in e||"Webkit"+up in e||"O"+up in e||"ms"+up in e};

		// window.addEventListener
			(function(){if("addEventListener"in window)return;window.addEventListener=function(type,f){window.attachEvent("on"+type,f)}})();

	// Play initial animations on page load.
		window.addEventListener('load', function() {
			window.setTimeout(function() {
				$body.classList.remove('is-preload');
			}, 100);
		});

	// Slideshow Background.
		(function() {

			// background images (need to declare this way because of django STATIC_URL)
				var img1 = GLOBAL_PATH + 'twitch_downloader/assets/images/bg01.jpg';
				var img2 = GLOBAL_PATH + 'twitch_downloader/assets/images/bg02.jpg';
				var img3 = GLOBAL_PATH + 'twitch_downloader/assets/images/bg03.jpg';
			// Settings.
				var settings = {
					
					// Images (in the format of 'url': 'alignment').
						images: {
							[img1]: 'center',
							[img2]: 'right',
							[img3]: 'right',
						},

					// Delay.
						delay: 6000
				};

			// Vars.
				var	pos = 0, lastPos = 0,
					$wrapper, $bgs = [], $bg,
					k, v;

			// Create BG wrapper, BGs.
				$wrapper = document.createElement('div');
					$wrapper.id = 'bg';
					$body.appendChild($wrapper);

				for (k in settings.images) {

					// Create BG.
						$bg = document.createElement('div');
							$bg.style.backgroundImage = 'url("' + k + '")';
							$bg.style.backgroundPosition = settings.images[k];
							$wrapper.appendChild($bg);

					// Add it to array.
						$bgs.push($bg);

				}

			// Main loop.
				$bgs[pos].classList.add('visible');
				$bgs[pos].classList.add('top');

				// Bail if we only have a single BG or the client doesn't support transitions.
					if ($bgs.length == 1
					||	!canUse('transition'))
						return;

				window.setInterval(function() {

					lastPos = pos;
					pos++;

					// Wrap to beginning if necessary.
						if (pos >= $bgs.length)
							pos = 0;

					// Swap top images.
						$bgs[lastPos].classList.remove('top');
						$bgs[pos].classList.add('visible');
						$bgs[pos].classList.add('top');

					// Hide last image after a short delay.
						window.setTimeout(function() {
							$bgs[lastPos].classList.remove('visible');
						}, settings.delay / 2);

				}, settings.delay);

		})();

		(function() {
			var TxtRotate = function(el, toRotate, period) {
				this.toRotate = toRotate;
				this.el = el;
				this.loopNum = 0;
				this.period = parseInt(period, 10) || 2000;
				this.txt = '';
				this.tick();
				this.isDeleting = false;
			  };
			  
			  TxtRotate.prototype.tick = function() {
				var i = this.loopNum % this.toRotate.length;
				var fullTxt = this.toRotate[i];
				
				if (this.isDeleting) {
				  this.txt = fullTxt.substring(0, this.txt.length - 1);
				} else {
				  this.txt = fullTxt.substring(0, this.txt.length + 1);
				}
			  
				this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';
			  
				var that = this;
				var delta = 175 - Math.random() * 100;
			  
				if (this.isDeleting) { delta /= 2; }
			  
				if (!this.isDeleting && this.txt === fullTxt) {
				  delta = this.period;
				  this.isDeleting = true;
				} else if (this.isDeleting && this.txt === '') {
				  this.isDeleting = false;
				  this.loopNum++;
				  delta = 500;
				}
			   
				setTimeout(function() {
				  that.tick();
				}, delta);
			  };

			  function shuffle(array) {
				var m = array.length, t, i;
			  
				// While there remain elements to shuffle…
				while (m) {
			  
				  // Pick a remaining element…
				  i = Math.floor(Math.random() * m--);
			  
				  // And swap it with the current element.
				  t = array[m];
				  array[m] = array[i];
				  array[i] = t;
				}
			  
				return array;
			  }
			  
			  window.onload = function() {
				var elements = document.getElementsByClassName('txt-rotate');
				for (var i=0; i<elements.length; i++) {
				  var toRotate = elements[i].getAttribute('data-rotate');
				  var period = elements[i].getAttribute('data-period');

				  if (toRotate) {
					  
					let shuffled = shuffle(JSON.parse(toRotate))
					new TxtRotate(elements[i], shuffled, period);
				  }
				}
				// INJECT CSS
				//var css = document.createElement("style");
				//css.type = "text/css";
				//css.innerHTML = ".txt-rotate > .wrap { border-right: 0.08em solid #666 }";
				//document.body.appendChild(css);
			  };
		})();
})();
