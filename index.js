const worker = perspective.worker();
const URL = "ws://localhost:8888/websocket";
const websocket = perspective.websocket(URL);
const datasource = async (table_name) => {
  const server_table = websocket.open_table(table_name);
  const server_view = await server_table.view();
  return worker.table(server_view);
//   return server_table
};

window.addEventListener("DOMContentLoaded", async function () {
  const workspace = document.getElementsByTagName("perspective-workspace")[0];
  workspace.addTable("holdings", datasource("data_source_one"));
  workspace.addTable("charts", datasource("data_source_one"));
  const config = {
    sizes: [1],
    detail: {
      main: {
        type: "split-area",
        orientation: "vertical",
        children: [
          {
            type: "tab-area",
            widgets: ["PERSPECTIVE_GENERATED_ID_1"],
            currentIndex: 0,
          },
          {
            type: "tab-area",
            widgets: ["PERSPECTIVE_GENERATED_ID_4"],
            currentIndex: 0,
          },
        ],
        sizes: [0.5031217481789803, 0.49687825182101975],
      },
    },
    mode: "globalFilters",
    viewers: {
      PERSPECTIVE_GENERATED_ID_1: {
        plugin: "datagrid",
        "row-pivots": ["sym"],
        // "column-pivots": ["sym"],
        columns: ["price","qty"],
        selectable: null,
        editable: null,
        // "computed-columns": null,
        // aggregates: null,
        // filters: null,
        // sort: null,
        // plugin_config: {
        //   realValues: ["price"],
        // },
        // master: false,
        name: "holdings",
        table: "holdings",
        // linked: false,
      },
      PERSPECTIVE_GENERATED_ID_4: {
        plugin: "datagrid",
        // "computed-columns": ['"quantity" * "close" as "value"'],
        "row-pivots": ["sym"],
        // "column-pivots": ["sym"],
        columns: ["price","qty"],
        selectable: null,
        editable: null,
        // aggregates: null,
        // filters: null,
        // sort: null,
        // plugin_config: {
        //   realValues: ["value"],
        // },
        // master: false,
        name: "Portfolio Value by Symbol, last 5 years",
        table: "charts",
        linked: false,
      },
    },
  };
  workspace.restore(config);
});
