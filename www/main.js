$(function(){
	var addDisplay = function(params){
		if(params.text == null){
			return;
		}
		if(params.isInput){
			var prefix = '>>> ';
		}
		else{
			var prefix = '';
		}
		var entry = $('<span></span>')
			.text(prefix + params.text + '\n')
			.appendTo(display);
		if(params.isError){
			entry.addClass('error');
		}
		display[0].scrollTop = display[0].scrollHeight;
	}

	var display = $('<div class="display"></div>')
		.appendTo('body');

	var sendInput = function(value){
		var xhr = new XMLHttpRequest();
		xhr.open('POST', '/', true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.send(JSON.stringify({text:value}));
		xhr.onload = function(){
			var response = JSON.parse(xhr.response);
			addDisplay(response);
		}
	}

	var history = [];
	var historyLocation = 0;

	var input = $('<input placeholder=">>>"></input>')
		.appendTo('body')
		.keydown(function(event){
			if(event.key == 'Enter'){
				var value = input.val();
				input.val('');
				addDisplay({text:value, isInput:true});
				sendInput(value);
				history.push(value);
				historyLocation = history.length;
			}
			else if(event.key == 'ArrowDown'){
				historyLocation += 1;
				if(historyLocation < history.length){
					input.val(history[historyLocation]);
				}
				else{
					historyLocation = history.length;
					input.val('');
				}
			}
			else if(event.key == 'ArrowUp'){
					historyLocation -= 1;
					if(historyLocation < 0){
						historyLocation = 0;
					}
					else{
						input.val(history[historyLocation]);
					}
			}
			else if(event.key == 'Escape'){
				historyLocation = history.length;
				input.val('');
			}
		});
})