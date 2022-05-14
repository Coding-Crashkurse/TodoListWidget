from datetime import datetime as dt


class PyRow(PyItemTemplate):
    def on_click(self, event):
        console.log(event.target)

        if event.target.classList.contains("checkme"):
            self.data["done"] = not self.data["done"]
            self.strike(self.data["done"])
        if event.target.classList.contains("fa-trash"):
            self.delete()


    def strike(self, value, extra=None):
        print(self.data)
        if value:
            self.element.classList.add("line-through")
            self.element.classList.add("text-green-700")
        else:
            self.element.classList.remove("line-through")
            self.element.classList.remove("text-green-700")


    def delete(self, extra=None):
        elem = document.getElementById(self._id)
        elem.parentNode.removeChild(elem)


    def add_date(self):
        return self.data["created_at"]


    def create(self):
        console.log("creating section")
        new_child = create("tr", self._id, "task bg-white my-1")
        console.log("creating values")

        console.log("creating innerHtml")
        new_child._element.innerHTML = dedent(
            f"""
                <td class='checkme'>{self.render_content()}</td>
                <td>{self.add_date()}</td>
                <td><i class="fa fa-trash" aria-hidden="true"></i></td>
            """
        )

        console.log("returning")
        return new_child




class PyTable(PyListTemplate):
    item_class = PyRow
    theme = None

    def connect(self):
        self.md = main_div = document.createElement("table")
        main_div.id = self._id + "-list-tasks-container"
        tr = document.createElement("tr")
        th1 = document.createElement("th")
        th2 = document.createElement("th")
        th3 = document.createElement("th")
        th1.innerText = "Todo"
        th2.innerText = "Erstellungsdatum"
        th3.innerText = "Löschen?"
        tr.appendChild(th1)
        tr.appendChild(th2)
        tr.appendChild(th3)

        self.md.appendChild(tr)

        if self.theme:
            self.theme.theme_it(main_div)

        self.parent.appendChild(main_div)

    def add(self, item):
        if isinstance(item, str):
            item = {"content": item, "done": True, "created_at": dt.now().strftime("%Y-%m-%d %H:%M")}

        super().add(item, labels=["content"], state_key="done")