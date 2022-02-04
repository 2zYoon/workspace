#define ee )
#define eee (
#define eeee ;
#define eeeee void
#define eeeeee }
#define eeeeeee {
#define eeeeeeee struct
#define eeeeeeeee long
#define eeeeeeeeee *
#define eeeeeeeeeee ,
#define eeeeeeeeeeee inline
#define eeeeeeeeeeeee static
#define eeeeeeeeeeeeee time_travel_event
#define eeeeeeeeeeeeeee time_travel_mode
#define eeeeeeeeeeeeeeee fn
#define eeeeeeeeeeeeeeeee fd
#define eeeeeeeeeeeeeeeeee unsigned
#define eeeeeeeeeeeeeeeeeee int
#define eeeeeeeeeeeeeeeeeeee e
#define eeeeeeeeeeeeeeeeeeeee TT_MODE_EXTERNAL
#define eeeeeeeeeeeeeeeeeeeeee duration
#define eeeeeeeeeeeeeeeeeeeeeee ==
#define eeeeeeeeeeeeeeeeeeeeeeee d
#define eeeeeeeeeeeeeeeeeeeeeeeee time_travel_propagate_time
#define eeeeeeeeeeeeeeeeeeeeeeeeee if
#define eeeeeeeeeeeeeeeeeeeeeeeeeee time_travel_wait_readable
#define eeeeeeeeeeeeeeeeeeeeeeeeeeee time_travel_sleep
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeee __time_travel_wait_readable
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeee enum
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee __time_travel_propagate_time
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee time
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee bool
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee TT_MODE_OFF
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee onstack
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee extern
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee TT_MODE_BASIC
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee list_head
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee list
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee nsec
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee TT_MODE_INFCPU
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee time_travel_add_irq_event
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee pending
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee time_travel_ndelay
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee time_travel_set_event_fn
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ->
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee =





#ifndef __TIMER_INTERNAL_H__

#define __TIMER_INTERNAL_H__

#include <linux/list.h>


#define TIMER_MULTIPLIER 256

#define TIMER_MIN_DELTA  500

eeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeee eeeeeee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeee 
eeeeeeeeeeeeeeeeeeeee eeeeeeeeeee 
eeeeee eeee 


#ifdef CONFIG_UML_TIME_TRAVEL_SUPPORT
eeeeeeee eeeeeeeeeeeeee eeeeeee 
eeeeeeeeeeeeeeeeee eeeeeeeee eeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeee 
eeeee eee eeeeeeeeee eeeeeeeeeeeeeeee ee eee eeeeeeee eeeeeeeeeeeeee eeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeee ee eeee 
eeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeee 
eeeeee eeee 

eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeee eeeeeeeeeeeeeee eeee 

eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeee eeeeeeeee eeeeeeeee eeeeeeeeeeeeeeeeeeeeee ee eeee 

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeee eeeeeeeeeeeeee eeeeeeeeee eeeeeeeeeeeeeeeeeeee eeeeeeeeeee 
eeeee eee eeeeeeeeee eeeeeeeeeeeeeeee ee eee eeeeeeee eeeeeeeeeeeeee eeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeee ee ee 
eeeeeee 
eeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeee eeee 
eeeeee 

eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeee ee eeee 

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeee eee eeeee ee 
eeeeeee 
eeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeee ee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee ee eeee 
eeeeee 

eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeee ee eeee 

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeee ee 
eeeeeee 
eeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeee ee 
eeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeee ee eeee 
eeeeee 

eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeee eeeeeeeeeeeeee eeeeeeeeee eeeeeeeeeeeeeeeeeeee ee eeee 

#else
eeeeeeee eeeeeeeeeeeeee eeeeeee 
eeeeee eeee 


#define time_travel_mode TT_MODE_OFF

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeee eeeeeeeee eeeeeeeee eeeeeeeeeeeeeeeeeeeeee ee 
eeeeeee 
eeeeee 



#define time_travel_set_event_fn(e, fn) do {} while (0)

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeee eee eeeee ee 
eeeeeee 
eeeeee 

eeeeeeeeeeeee eeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeee ee 
eeeeeee 
eeeeee 

#endif /* CONFIG_UML_TIME_TRAVEL_SUPPORT */


eeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee eee eeeeeeeeeeeeeeeeee eeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ee eeee 

#endif /* __TIMER_INTERNAL_H__ */

