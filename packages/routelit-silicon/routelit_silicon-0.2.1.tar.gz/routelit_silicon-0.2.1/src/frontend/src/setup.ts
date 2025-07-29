import { componentStore } from "routelit-client";
import './silicon.min.css'
import './lib.css'
import {
  Root,
  Sidebar,
  Main,
} from "./components";

componentStore.register("root", Root);
componentStore.register("sidebar", Sidebar);
componentStore.register("main", Main);
componentStore.forceUpdate();
