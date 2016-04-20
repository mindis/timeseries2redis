# timeseries2redis
python pandas timeseries to redis read/ write functionality

	>>>> from timeseries2redis import TickData
	>>>> ts = TickData("B")

	>>>> ts.get(-5)
	>>>> ask	bid	count	volume
	>>>> date				
	>>>> 2016-04-20 13:02:32	31	31	1	1000
	>>>> 2016-04-20 13:02:32	34	34	1	1000
	>>>> 2016-04-20 13:02:32	48	48	1	1000
	>>>> 2016-04-20 13:02:32	11	11	1	1000
	>>>> 2016-04-20 13:02:32	35	35	1	1000