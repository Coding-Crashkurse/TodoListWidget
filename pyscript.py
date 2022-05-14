class PyWidgetTheme:
    def __init__(self, main_style_classes):
        self.main_style_classes = main_style_classes

    def theme_it(self, widget):
        for klass in self.main_style_classes.split(" "):
            widget.classList.add(klass)


class PyItemTemplate(Element):
    label_fields = None

    def __init__(self, data, labels=None, state_key=None, parent=None):
        self.data = data

        self.register_parent(parent)

        if not labels:
            labels = list(self.data.keys())
        self.labels = labels

        self.state_key = state_key

        super().__init__(self._id)

    def register_parent(self, parent):
        self._parent = parent
        if parent:
            self._id = f"{self._parent._id}-c-{len(self._parent._children)}"
            self.data["id"] = self._id
        else:
            self._id = None

    def create(self):
        console.log("creating section")
        new_child = create("section", self._id, "task bg-white my-1")
        console.log("creating values")

        console.log("creating innerHtml")
        new_child._element.innerHTML = dedent(
            f"""
            <label for="flex items-center p-2 ">
              <input class="mr-2" type="checkbox" class="task-check">
              <p class="m-0 inline">{self.render_content()}</p>
            </label>
            """
        )

        console.log("returning")
        return new_child

    def on_click(self, evt):
        pass

    def pre_append(self):
        pass

    def post_append(self):
        self.element.click = self.on_click
        self.element.onclick = self.on_click

        self._post_append()

    def _post_append(self):
        pass

    def strike(self, value, extra=None):
        if value:
            self.add_class("line-through")
        else:
            self.remove_class("line-through")

    def render_content(self):
        return " - ".join([self.data[f] for f in self.labels])


class PyListTemplate:
    theme = PyWidgetTheme("flex flex-col-reverse mt-8 mx-8")
    item_class = PyItemTemplate

    def __init__(self, parent):
        self.parent = parent
        self._children = []
        self._id = self.parent.id

    @property
    def children(self):
        return self._children

    @property
    def data(self):
        return [c.data for c in self._children]

    def render_children(self):
        binds = {}
        for i, c in enumerate(self._children):
            txt = c.element.innerHTML
            rnd = str(time.time()).replace(".", "")[-5:]
            new_id = f"{c.element.id}-{i}-{rnd}"
            binds[new_id] = c.element.id
            txt = txt.replace(">", f" id='{new_id}'>")
            print(txt)

        def foo(evt):
            console.log(evt)
            evtEl = evt.srcElement
            srcEl = Element(binds[evtEl.id])
            srcEl.element.onclick()
            evtEl.classList = srcEl.element.classList

        for new_id in binds:
            Element(new_id).element.onclick = foo

    def connect(self):
        self.md = main_div = document.createElement("div")
        main_div.id = self._id + "-list-tasks-container"

        if self.theme:
            self.theme.theme_it(main_div)

        self.parent.appendChild(main_div)

    def add(self, *args, **kws):
        if not isinstance(args[0], self.item_class):
            child = self.item_class(*args, **kws)
        else:
            child = args[0]
        child.register_parent(self)
        return self._add(child)

    def _add(self, child_elem):
        console.log("appending child", child_elem.element)
        self.pre_child_append(child_elem)
        child_elem.pre_append()
        self._children.append(child_elem)
        self.md.appendChild(child_elem.create().element)
        child_elem.post_append()
        self.child_appended(child_elem)
        return child_elem

    def pre_child_append(self, child):
        pass

    def child_appended(self, child):
        """Overwrite me to define logic"""
        pass

