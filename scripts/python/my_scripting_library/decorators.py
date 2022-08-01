from functools import wraps


class do_for_each_in_list(object):
  
   def __init__(self, func):
        self.func = func
        wraps(func)(self)

   def __call__(self, *args, **kwargs):
        if type(args[0]) == list:
            print 'made it here'
            this_list = args[0]
            new_list = []
            for item in this_list:
                new_args_list = [item]
                for thing in args[1:]:
                    new_args_list.append(thing)
                new_args = tuple(new_args_list)
                new_list.append(self.func(*new_args))
            return new_list
        else:
            ret = self.func(*args, **kwargs)
            return ret