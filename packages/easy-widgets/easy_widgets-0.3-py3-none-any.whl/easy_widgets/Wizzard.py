
from .Widget import * 
from .Menu import * 
from .TextInput import * 
from .Application import * 

class Wizzard():

    def __init__(self, parent, pages=[], **params):
        """
        pages: list of tuples with:
        type: one of "choice", "input", "param"
        param: parameter name to be set after executing this step
        text: text to be shown on this page
        params: custom params to page

        Parameters for types:

        choice: 
        "choices": list of tuples where every pair contains (value, description)

        param:
        func: function which recieves one argument, value of given param
        """
        self.pages = pages 
        self.params = params
        self.parent = parent


    def withPage(self, pagetype, param, text, params):
        return Wizzard(self.parent, self.pages + [(pagetype, param, text, params)],**self.params)

    def show(self):
        if self.pages == []:
            self.parent.show()
        else:
            head, *tail = self.pages
            pagetype, param, text, params = head 
            if pagetype == "param":
                params.get("func", lambda v: None)(self.params.get(param, None))
                Wizzard(
                    self.parent, tail,
                    **self.params 
                ).show()
            elif pagetype == "choice":
                menu = Menu(text)
                for v,d in params.get("choices", []):
                    menu.addOption(d,  lambda b,p: Wizzard(
                        self.parent, tail, 
                        **{k: vv for k,vv in list(self.params.items()) + [(p[0], p[1])]}
                    ).show(),
                    params=[param, v])
                menu.show()
            elif pagetype == "input":
                TextInput(text, lambda ans: Wizzard(
                    self.parent,
                    tail,
                    **{k: vv for k,vv in list(self.params.items()) + [(param, ans)]}
                ).show()).show()
            else:
                raise TypeError("Wrong page type")
    def withInput(self, text, param):
        return self.withPage("input", param, text, {})

    def withChoices(self, text, param, choices):
        """
        Choices: list of tuples (value, description)
        """
        return self.withPage("choice", param, text, {"choices": choices})
    
    def withParam(self, param, func):
        return self.withPage("param", param, param, {"func": func})
