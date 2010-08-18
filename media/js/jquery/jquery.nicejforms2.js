/*#############################################################
Name: NiceJForms
Version: 2.0
Author: Lucian Lature
WTF: Plugin for jQuery

Feel free to use and modify but please keep this copyright intact.
#################################################################*/

(function($){
	$.fn.NiceJFormer = function(options) {

		var global = this;
		
		//Theme Variables - edit these to match your theme
		var defaults = {  
			imagesPath: "img/",  
			selectRightWidthSimple: 19,  
			selectRightWidthScroll: 2,  
			selectMaxHeight: 200,  
			textareaTopPadding: 10,  
			textareaSidePadding: 10  
		};  
  
		var options = $.extend(defaults, options); 

		//Global Variables
		var resizeTest = 1;
		
		if($.browser.msie && $.browser.version < "7.0") return false; //exit script if IE6 or below
			
		this.niceInputText = function(el) { // transform Text inputs
			
			el.oldClassName = el.className;
			
			el.left = document.createElement('img');
			$(el.left).attr({src: options.imagesPath + "0.png"}).addClass('NFTextLeft');
			el.right = document.createElement('img');
			$(el.right).attr({src: options.imagesPath + "0.png"}).addClass('NFTextRight');
			el.dummy = document.createElement('div');
			$(el.dummy).addClass('NFTextCenter');
			
			
			el.init = function() {
				
				// we should use the line below, but the wrap() function is broken, clone(true) has no effect and the reference is lost
				// $(this).before(this.left).after(this.right).wrap(this.dummy).removeClass().addClass("NFText");
				
				this.parentNode.insertBefore(this.left, this);
				this.parentNode.insertBefore(this.right, this.nextSibling);
				this.dummy.appendChild(this);
				this.right.parentNode.insertBefore(this.dummy, this.right);
				this.className = "NFText";
				
			}
			
			$(el).bind('focus', function(){
				$(this.dummy).removeClass().addClass('NFTextCenter NFh');
				$(this.left).removeClass().addClass('NFTextLeft NFh');
				$(this.right).removeClass().addClass('NFTextRight NFh');
			});
			
			$(el).bind('blur', function(){
				$(this.dummy).removeClass().addClass('NFTextCenter');
				$(this.left).removeClass().addClass('NFTextLeft');
				$(this.right).removeClass().addClass('NFTextRight');
			});
			
			
			el.unload = function() {
				this.parentNode.parentNode.appendChild(this);
				this.parentNode.removeChild(this.left);
				this.parentNode.removeChild(this.right);
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			};
	
			return el;
	
		};
		
		this.niceInputRadio = function(el) { //extent Radio buttons
			
			el.oldClassName = el.className;
			el.dummy = document.createElement('div');
			if(el.checked) {
				$(el.dummy).addClass("NFRadio NFh");
			} else {
				$(el.dummy).addClass("NFRadio");
			}
			el.dummy.ref = el;
			
			$(el.dummy).css({ left: $(el).position().left + 4 + 'px', top: $(el).position().top + 4 + 'px' });
			
			$(el.dummy).bind('click', function(){
				
				if(!this.ref.checked) {
					
					$('input[name=' + this.ref.name + ']').each(function(){
						this.checked = false;
						$(this.dummy).removeClass().addClass('NFRadio');
					});
					
					this.ref.checked = true;
					this.className = "NFRadio NFh";
				}
			});
			
			
			$(el)
				.bind('click', function() {
					if(this.checked) {
						$('input[name=' + this.name + ']').each(function(){
							$(this.dummy).removeClass().addClass('NFRadio');
						});
						this.dummy.className = "NFRadio NFh";
					}
				})
				.bind('focus', function() {
					$(this.dummy).addClass('NFfocused');
				})
				.bind('blur', function() {
					this.dummy.className = this.dummy.className.replace(/ NFfocused/g, "");
				});
			
			el.init = function() {
				$(this).before(this.dummy).addClass("NFhidden");
			}
			
			el.unload = function() {
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			}
			
			return el;
		}
		
		this.niceInputCheck = function(el) { //extend Checkboxes
			
			el.oldClassName = el.className;
			
			el.dummy = document.createElement('img');
			$(el.dummy).attr({src: options.imagesPath + "0.png"});
			
			if(el.checked) {
				$(el.dummy).addClass('NFCheck NFh');
			} else {
				$(el.dummy).addClass('NFCheck');
			}
			el.dummy.ref = el;

			$(el.dummy).css({ left: $(el).position().left + 4 + 'px', top: $(el).position().top + 4 + 'px' });

			
			$(el.dummy)
				.bind('click', function(){
					if(!this.ref.checked) {
						this.ref.checked = true;
						$(this).removeClass().addClass("NFCheck NFh");
					} else {
						this.ref.checked = false;
						$(this).removeClass().addClass("NFCheck");
					}
				});
			
			$(el)
				.bind('click', function(){
					if(this.checked) {
						$(this.dummy).removeClass().addClass("NFCheck NFh");
					} else {
						$(this.dummy).removeClass().addClass("NFCheck");
					}
				})
				.bind('focus', function(){
					$(this.dummy).addClass("NFfocused");
				})
				.bind('blur', function(){
					this.dummy.className = this.dummy.className.replace(/ NFfocused/g, "");
				})
			
			el.init = function() {
				$(this).before($(this.dummy)).removeClass().addClass('NFhidden');
			} 
			el.unload = function() {
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			}
			
			return el;
		}
		
		this.niceInputSubmit = function(el) { //extend Buttons
			
			el.oldClassName = el.className;
			el.left = document.createElement('img');
			$(el.left).attr({src: options.imagesPath + "0.png"}).addClass("NFButtonLeft");
			el.right = document.createElement('img');
			$(el.right).attr({src: options.imagesPath + "0.png"}).addClass("NFButtonRight");
		
			$(el)
				.bind('mouseover', function(){
					$(this).removeClass().addClass("NFButton NFh");
					$(this.left).removeClass().addClass("NFButtonLeft NFh");
					$(this.right).removeClass().addClass("NFButtonRight NFh");
				})
				.bind('mouseout', function(){
					$(this).removeClass().addClass("NFButton");
					$(this.left).removeClass().addClass("NFButtonLeft");
					$(this.right).removeClass().addClass("NFButtonRight");
				})
					
			el.init = function() {
				$(this).before(this.left).after(this.right).removeClass().addClass("NFButton");
			}
			el.unload = function() {
				this.parentNode.removeChild(this.left);
				this.parentNode.removeChild(this.right);
				this.className = this.oldClassName;
			}
			
			return el;
		}
		
		this.niceInputFile = function(el) { //extend File inputs
			
			el.oldClassName = el.className;
			
			el.dummy = document.createElement('div');
			$(el.dummy).addClass("NFFile");
			
			el.file = document.createElement('div');
			$(el.file).addClass("NFFileNew");
			
			el.center = document.createElement('div');
			$(el.center).addClass("NFTextCenter");

			el.clone = document.createElement('input');
			$(el.clone).attr('type', 'text').addClass("NFText");
			el.clone.ref = el;
			
			el.left = document.createElement('img');
			$(el.left).attr({src: options.imagesPath + "0.png"}).addClass("NFTextLeft");
			el.button = document.createElement('img');
			$(el.button).attr({src: options.imagesPath + "0.png"}).addClass("NFFileButton");
			el.button.ref = el;
			$(el.button).bind('click', function(){ this.ref.click();});
			
			/*
			el.init = function() {
				
				var top = $(this).parent()[0];
				
				if($(this).prev()) {
					var where = $(this).prev()[0];
				} else {
					var where = top.childNodes[0];
				}
				
				// we should use the lines below, but the wrap() function is broken, clone(true) has no effect and the reference is lost
				// $(this.file).append(this.clone);
				// $(this.clone).before(this.left).after(this.button).wrap(this.center);
				// $(this).wrap(this.dummy).after(this.file).removeClass().addClass("NFhidden");
				
				top.insertBefore(this.dummy, where);
				this.dummy.appendChild(this);
				this.center.appendChild(this.clone);
				this.file.appendChild(this.center);
				this.file.insertBefore(this.left, this.center);
				this.file.appendChild(this.button);
				this.dummy.appendChild(this.file);
				
				this.className = "NFhidden";
				this.relatedElement = this.clone;
			}
			*/
			
			/*
			el.unload = function() {
				this.parentNode.parentNode.appendChild(this);
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			}
			
			
			el.onchange = el.onmouseout = function() {this.relatedElement.value = this.value;}
			
			$(el)
				//.bind('change', function() {
				//	this.relatedElement.value = this.value;
				//})
				//.bind('mouseout', function() {
				//	this.relatedElement.value = this.value;
				//})
				.bind('focus', function() {
					$(this.left).addClass("NFh");
					$(this.center).addClass("NFh");
					$(this.button).addClass("NFh");
				})
				.bind('blur', function() {
					$(this.left).removeClass().addClass("NFTextLeft");
					$(this.center).removeClass().addClass("NFTextCenter");
					$(this.button).removeClass().addClass("NFFileButton");
				})
				.bind('select', function() {
					this.relatedElement.select();
					this.value = '';
				})
			*/
			
			//el.oldClassName = el.className;
			//el.dummy = document.createElement('div');
			//el.dummy.className = "NFFile";
			//el.file = document.createElement('div');
			//el.file.className = "NFFileNew";
			//el.center = document.createElement('div');
			//el.center.className = "NFTextCenter";
			//el.clone = document.createElement('input');
			//el.clone.type = "text";
			//el.clone.className = "NFText";
			//el.clone.ref = el;
			//el.left = document.createElement('img');
			//el.left.src = options.imagesPath + "0.png";
			//el.left.className = "NFTextLeft";
			//el.button = document.createElement('img');
			//el.button.src = options.imagesPath + "0.png";
			//el.button.className = "NFFileButton";
			//el.button.ref = el;
			//el.button.onclick = function() {this.ref.click();}
			
			el.init = function() {
				//var top = this.parentNode;
				var top = $(this).parent()[0];
				// if(this.previousSibling) {var where = this.previousSibling;}
				// else {var where = top.childNodes[0];}
				
				if($(this).prev()) {
					var where = this.previousSibling;
				} else {
					var where = top.childNodes[0];
				}
				
				// we should use the lines below, but the wrap() function is broken, clone(true) has no effect and the reference is lost
				// $(this.file).append(this.clone);
				// $(this.clone).before(this.left).after(this.button).wrap(this.center);
				// $(this).wrap(this.dummy).after(this.file).removeClass().addClass("NFhidden");
				
				top.insertBefore(this.dummy, where);
				this.dummy.appendChild(this);
				this.center.appendChild(this.clone);
				this.file.appendChild(this.center);
				this.file.insertBefore(this.left, this.center);
				this.file.appendChild(this.button);
				this.dummy.appendChild(this.file);
				
				this.className = "NFhidden";
				this.relatedElement = this.clone;
				
			}
			
			el.unload = function() {
				this.parentNode.parentNode.appendChild(this);
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			}
			el.onchange = el.onmouseout = function() {this.relatedElement.value = this.value;}
			el.onfocus = function() {
				this.left.className = "NFTextLeft NFh";
				this.center.className = "NFTextCenter NFh";
				this.button.className = "NFFileButton NFh";
			}
			el.onblur = function() {
				this.left.className = "NFTextLeft";
				this.center.className = "NFTextCenter";
				this.button.className = "NFFileButton";
			}
			el.onselect = function() {
				this.relatedElement.select();
				this.value = '';
			}
			
			return el;
		}
		
		
		this.niceTextarea = function(el) { //extend Textareas
			
			el.oldClassName = el.className;
			el.height = el.offsetHeight - options.textareaTopPadding;
			el.width = el.offsetWidth - options.textareaSidePadding;
			
			el.topLeft = document.createElement('img');
			$(el.topLeft).attr({src: options.imagesPath + "0.png"}).addClass("NFTextareaTopLeft");
			el.topRight = document.createElement('div');
			$(el.topRight).addClass("NFTextareaTop");
			el.bottomLeft = document.createElement('img');
			$(el.bottomLeft).attr({src: options.imagesPath + "0.png"}).addClass("NFTextareaBottomLeft");
			el.bottomRight = document.createElement('div');
			$(el.bottomRight).addClass("NFTextareaBottom");

			el.left = document.createElement('div');
			$(el.left).addClass("NFTextareaLeft");
			el.right = document.createElement('div');
			$(el.right).addClass("NFTextareaRight");
			
			el.init = function() {
				var top = this.parentNode;
				if(this.previousSibling) {var where = this.previousSibling;}
				else {var where = top.childNodes[0];}
				top.insertBefore(el.topRight, where);
				top.insertBefore(el.right, where);
				top.insertBefore(el.bottomRight, where);
				this.topRight.appendChild(this.topLeft);
				this.right.appendChild(this.left);
				this.right.appendChild(this);
				this.bottomRight.appendChild(this.bottomLeft);
				el.style.width = el.topRight.style.width = el.bottomRight.style.width = el.width + 'px';
				el.style.height = el.left.style.height = el.right.style.height = el.height + 'px';
				this.className = "NFTextarea";
			}
			
			el.unload = function() {
				this.parentNode.parentNode.appendChild(this);
				this.parentNode.removeChild(this.topRight);
				this.parentNode.removeChild(this.bottomRight);
				this.parentNode.removeChild(this.right);
				this.className = this.oldClassName;
				this.style.width = this.style.height = "";
			}
			
			$(el)
				.bind('focus', function() {
					this.topLeft.className = "NFTextareaTopLeft NFh";
					this.topRight.className = "NFTextareaTop NFhr";
					this.left.className = "NFTextareaLeftH";
					this.right.className = "NFTextareaRightH";
					this.bottomLeft.className = "NFTextareaBottomLeft NFh";
					this.bottomRight.className = "NFTextareaBottom NFhr";
				})
				.bind('blur', function() {
					this.topLeft.className = "NFTextareaTopLeft";
					this.topRight.className = "NFTextareaTop";
					this.left.className = "NFTextareaLeft";
					this.right.className = "NFTextareaRight";
					this.bottomLeft.className = "NFTextareaBottomLeft";
					this.bottomRight.className = "NFTextareaBottom";
				});
			
			return el;
		}
		
		this.niceSelect = function(el) { //extend Selects
			
			el.oldClassName = el.className;
		
			el.dummy = document.createElement('div');
			el.dummy.ref = el;
			$(el.dummy).addClass("NFSelect").width($(el).width()).css({ left: $(el).position().left + 'px', top: $(el).position().top + 'px' });;
			
			el.left = document.createElement('img');
			$(el.left).attr({src: options.imagesPath + "0.png"}).addClass("NFSelectLeft");
			el.right = document.createElement('div');
			$(el.right).addClass("NFSelectRight");
			
			el.txt = document.createTextNode(el.options[0].text);
			el.bg = document.createElement('div');
			$(el.bg).addClass("NFSelectTarget").css({'display': 'none'});
			
			el.opt = document.createElement('ul');
			$(el.opt).addClass("NFSelectOptions");
			
			el.opts = new Array(el.options.length);
			
			el.init = function(pos) {
				
				this.dummy.appendChild(this.left);
				this.right.appendChild(this.txt);
				this.dummy.appendChild(this.right);
				this.bg.appendChild(this.opt);
				this.dummy.appendChild(this.bg);
				
				for(var q = 0; q < this.options.length; q++) {
					this.opts[q] = new global.option(this.options[q], q);
					this.opt.appendChild(this.options[q].li);
					this.options[q].lnk.onclick = function() {
						this._onclick();
						$('div', this.ref.dummy)[0].innerHTML = this.ref.options[this.pos].text;
						// this.ref.dummy.getElementsByTagName('div')[0].innerHTML = this.ref.options[this.pos].text;
						this.ref.options[this.pos].selected = "selected";
						for(var w = 0; w < this.ref.options.length; w++) {this.ref.options[w].lnk.className = "";}
						this.ref.options[this.pos].lnk.className = "NFOptionActive";
					}
				}
				if(this.options.selectedIndex) {
					$('div', this.dummy)[0].innerHTML = this.options[this.options.selectedIndex].text;					
					this.options[this.options.selectedIndex].lnk.className = "NFOptionActive";
				}
				this.dummy.style.zIndex = 999 - pos;
				this.parentNode.insertBefore(this.dummy, this);
				this.className = "NFhidden";
			}
			
			el.unload = function() {
				this.parentNode.removeChild(this.dummy);
				this.className = this.oldClassName;
			}
			el.dummy.onclick = function() {
				var allDivs = document.getElementsByTagName('div'); for(var q = 0; q < allDivs.length; q++) {if((allDivs[q].className == "NFSelectTarget") && (allDivs[q] != this.ref.bg)) {allDivs[q].style.display = "none";}}
				if(this.ref.bg.style.display == "none") {this.ref.bg.style.display = "block";}
				else {this.ref.bg.style.display = "none";}
				if(this.ref.opt.offsetHeight > options.selectMaxHeight) {
					this.ref.bg.style.width = this.ref.offsetWidth - options.selectRightWidthScroll + 33 + 'px';
					this.ref.opt.style.width = this.ref.offsetWidth - options.selectRightWidthScroll + 'px';
				}
				else {
					this.ref.bg.style.width = this.ref.offsetWidth - options.selectRightWidthSimple + 33 + 'px';
					this.ref.opt.style.width = this.ref.offsetWidth - options.selectRightWidthSimple + 'px';
				}
			}
			el.bg.onmouseout = function(e) {
				if (!e) var e = window.event;
				e.cancelBubble = true;
				if (e.stopPropagation) e.stopPropagation();
				var reltg = (e.relatedTarget) ? e.relatedTarget : e.toElement;
				if((reltg.nodeName == 'A') || (reltg.nodeName == 'LI') || (reltg.nodeName == 'UL')) return;
				if((reltg.nodeName == 'DIV') || (reltg.className == 'NFSelectTarget')) return;
				else{this.style.display = "none";}
			}
			el.dummy.onmouseout = function(e) {
				if (!e) var e = window.event;
				e.cancelBubble = true;
				if (e.stopPropagation) e.stopPropagation();
				var reltg = (e.relatedTarget) ? e.relatedTarget : e.toElement;
				if((reltg.nodeName == 'A') || (reltg.nodeName == 'LI') || (reltg.nodeName == 'UL')) return;
				if((reltg.nodeName == 'DIV') || (reltg.className == 'NFSelectTarget')) return;
				else{this.ref.bg.style.display = "none";}
			}
			el.onfocus = function() {this.dummy.className += " NFfocused";}
			el.onblur = function() {this.dummy.className = this.dummy.className.replace(/ NFfocused/g, "");}
			el.onkeydown = function(e) {
				if (!e) var e = window.event;
				var thecode = e.keyCode;
				var active = this.selectedIndex;
				switch(thecode){
					case 40: //down
						if(active < this.options.length - 1) {
							for(var w = 0; w < this.options.length; w++) {this.options[w].lnk.className = "";}
							var newOne = active + 1;
							this.options[newOne].selected = "selected";
							this.options[newOne].lnk.className = "NFOptionActive";
							this.dummy.getElementsByTagName('div')[0].innerHTML = this.options[newOne].text;
						}
						return false;
						break;
					case 38: //up
						if(active > 0) {
							for(var w = 0; w < this.options.length; w++) {this.options[w].lnk.className = "";}
							var newOne = active - 1;
							this.options[newOne].selected = "selected";
							this.options[newOne].lnk.className = "NFOptionActive";
							this.dummy.getElementsByTagName('div')[0].innerHTML = this.options[newOne].text;
						}
						return false;
						break;
					default:
						break;
				}
			}
			
			return el;
		}
		
		this.niceMultipleSelect = function(el) { //extend Multiple Selects
			el.oldClassName = el.className;
			el.height = el.offsetHeight;
			el.width = el.offsetWidth;
			el.topLeft = document.createElement('img');
			el.topLeft.src = options.imagesPath + "0.png";
			el.topLeft.className = "NFMultiSelectTopLeft";
			el.topRight = document.createElement('div');
			el.topRight.className = "NFMultiSelectTop";
			el.bottomLeft = document.createElement('img');
			el.bottomLeft.src = options.imagesPath + "0.png";
			el.bottomLeft.className = "NFMultiSelectBottomLeft";
			el.bottomRight = document.createElement('div');
			el.bottomRight.className = "NFMultiSelectBottom";
			el.left = document.createElement('div');
			el.left.className = "NFMultiSelectLeft";
			el.right = document.createElement('div');
			el.right.className = "NFMultiSelectRight";
			el.init = function() {
				var top = this.parentNode;
				if(this.previousSibling) {var where = this.previousSibling;}
				else {var where = top.childNodes[0];}
				top.insertBefore(el.topRight, where);
				top.insertBefore(el.right, where);
				top.insertBefore(el.bottomRight, where);
				this.topRight.appendChild(this.topLeft);
				this.right.appendChild(this.left);
				this.right.appendChild(this);
				this.bottomRight.appendChild(this.bottomLeft);
				el.style.width = el.topRight.style.width = el.bottomRight.style.width = el.width + 'px';
				el.style.height = el.left.style.height = el.right.style.height = el.height + 'px';
				el.className = "NFMultiSelect";
			}
			el.unload = function() {
				this.parentNode.parentNode.appendChild(this);
				this.parentNode.removeChild(this.topRight);
				this.parentNode.removeChild(this.bottomRight);
				this.parentNode.removeChild(this.right);
				this.className = this.oldClassName;
				this.style.width = this.style.height = "";
			}
			el.onfocus = function() {
				this.topLeft.className = "NFMultiSelectTopLeft NFh";
				this.topRight.className = "NFMultiSelectTop NFhr";
				this.left.className = "NFMultiSelectLeftH";
				this.right.className = "NFMultiSelectRightH";
				this.bottomLeft.className = "NFMultiSelectBottomLeft NFh";
				this.bottomRight.className = "NFMultiSelectBottom NFhr";
			}
			el.onblur = function() {
				this.topLeft.className = "NFMultiSelectTopLeft";
				this.topRight.className = "NFMultiSelectTop";
				this.left.className = "NFMultiSelectLeft";
				this.right.className = "NFMultiSelectRight";
				this.bottomLeft.className = "NFMultiSelectBottomLeft";
				this.bottomRight.className = "NFMultiSelectBottom";
			}
			
			return el;
		}
		
		this.option = function(el, no) { //extend Options
			el.li = document.createElement('li');
			el.lnk = document.createElement('a');
			el.lnk.href = "javascript:;";
			el.lnk.ref = el.parentNode;
			el.lnk.pos = no;
			el.lnk._onclick = el.onclick || function () {};
			el.txt = document.createTextNode(el.text);
			el.lnk.appendChild(el.txt);
			el.li.appendChild(el.lnk);
			
			return el;
		}
		
		return this.each(function() {
			
			form = $(this);
			
			$('input[type=text]', form).add($('input[type=password]', form)).each(function() {
				global.niceInputText(this).init();
			});
			
			$('input[type=radio]', form).each(function() {
				global.niceInputRadio(this).init();
			});
			
			$('input[type=checkbox]', form).each(function() {
				global.niceInputCheck(this).init();
			});
			
			$('input[type=submit]', form).add($('input[type=reset]', form)).add($('button', form)).each(function() {
				global.niceInputSubmit(this).init();
			});
			
			
			$('input[type=file]', form).each(function() {
				global.niceInputFile(this).init();
			});
			
			
			$('textarea', form).each(function() {
				global.niceTextarea(this).init();
			});
			
			
			$('select', form).each(function(index) {
				if(this.size > 1) {
					global.niceMultipleSelect(this).init();
				} else {
					global.niceSelect(this).init(index);
				}
			});
			
		});
		
	};
	
})(jQuery);