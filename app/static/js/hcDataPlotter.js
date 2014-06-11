$(function() {
	var seriesOptions = [],
		yAxisOptions = [],
		seriesCounter = 0,
		showPlot=true,
		names = [{%for i in streamList%}'{{i.streamID}}',{%endfor%}],
		TZoffset = moment().zone()*60*1000;
		colors = Highcharts.getOptions().colors;
		
		//need to split this out into its own function so data isnt loaded all at once
	$.each(names, function(i, name) {
		$.getJSON('/statistics/get_data/{{dev_id}}/'+name, function(data) {
			if (data.data.length>1) {
				for (var j=0; j< data.data.length; j++){
					data.data[j][0]-=TZoffset
				}
			}
			else {name =name+"(0)";}
			
			if (seriesCounter == {{idx}})
				{showPlot=true;}
			else
				{showPlot=false;}
			
			seriesOptions[i] = {
				name: name, 
				data: data.data,
				visible:showPlot,
			};
			// As we're loading the data asynchronously, we don't know what order it will arrive. So
			// we keep a counter and create the chart when all the data is loaded.
			seriesCounter++;
			if (seriesCounter == names.length) {
				createChart();
			}
		});
	});

	// create the chart when all data is loaded
	function createChart() {
		$('#container').highcharts('StockChart', {	
            title: {
                text: 'PG Data View'
            },		
		    chart: {
				events: {
					load: function(chart) {
						this.setTitle(null, {
							text: 'Built chart in '+ (new Date() - start) +'ms'
						});
					}
				},
				zoomType: 'xy'
		    },
            rangeSelector: {
                selected: 0,
                inputDateFormat: '%Y-%m-%d',
                buttons: [
					{	type: 'day',
						count: 1,
						text: '1D'
					},{	type: 'week',
						count: 1,
						text: 'Wk'
					},{	type: 'month',
						count: 1,
						text: '1M'
					},{
						type:'all',
						count:1,
						text:'All'
					}],				
            },			
		    yAxis: {
		    	//labels: {formatter: function() {return (this.value > 0 ? '+' : '') + this.value + '%';}},
		    	plotLines: [{
		    		value: 0,
		    		width: 2,
		    		color: 'silver'
		    	}]
		    },
            xAxis : {
                //events : {afterSetExtremes : afterSetExtremes},
                minRange: 3600 * 1000 // one hour
            },
			
			legend:{
				enabled: true,
				layout: 'vertical',
				backgroundColor: '#FFFFFF',
				//floating: true,
				align: 'left',
				x: 0,
				verticalAlign: 'top',
				y: 70
			},

			series: seriesOptions,
			
		    plotOptions: {
				//line:{events:{legendItemClick: legendItemClick},},
			},
		    tooltip: {
		    },

		    
		});
	}
	
});	

/**
 * Load new data depending on the selected min and max
 */
function afterSetExtremes(e) {
    var url,
        currentExtremes = this.getExtremes(),
        range = e.max - e.min;
    
    chart.showLoading('Loading data from server...');
    $.getJSON('http://www.highcharts.com/samples/data/from-sql.php?start='+ Math.round(e.min) +
            '&end='+ Math.round(e.max) +'&callback=?', function(data) {
        
        chart.series[0].setData(data);
        chart.hideLoading();
    });
    
}

function legendItemClick(e){
	alert(e.chart.name+"Legend")
	chart.series[0].setData(data);
}
