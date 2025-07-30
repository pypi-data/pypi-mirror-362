import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { INotebookTools, INotebookTracker } from '@jupyterlab/notebook';
import { YarnApplicationTableWidget } from "./widget"
import { Environment } from "./environment";
const WIDGET = { id: 'sagemaker-debugging' };

export const debuggingPlugin: JupyterFrontEndPlugin<void> = {
  id: WIDGET.id,
  description: 'JupyterLab extension to improve debugging experience in SageMaker.',
  requires: [INotebookTools, INotebookTracker],
  autoStart: true,
  activate: (app: JupyterFrontEnd, tools: INotebookTools, tracker: INotebookTracker) => {
    console.log('JupyterLab extension sagemaker-debugging is activated!');
    Environment.getInstance();
    const tableWidget = new YarnApplicationTableWidget();
    tableWidget.setListenerForNotebookChangeEvents(tracker);
    tableWidget.setCellExecutedSignal();
    tracker.currentChanged.connect(
      (tracker, panel) => tableWidget.onNotebookChange(tracker, panel),
      WIDGET
    );
    tracker.widgetAdded.connect(
      (tracker, panel) => tableWidget.onNotebookChange(tracker, panel),
      WIDGET
    );
  }
};

// export default debuggingPlugin;
