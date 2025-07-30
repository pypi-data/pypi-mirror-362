import { INotebookTracker } from '@jupyterlab/notebook/lib/tokens';
import $ from 'jquery';
import { NotebookActions, NotebookPanel } from '@jupyterlab/notebook';
import { LINK_TYPE_SPARK_UI, LINK_TYPE_DRIVER_LOG } from './constants';
import { getConnectionDetails } from './jupyter_api_client';
import { handleEMRonEc2DebuggingLinksClicked } from "./computes/emr_ec2";
import { handleEMRServerlessDebuggingLinksClicked } from "./computes/emr_serverless";
import { handleGlueDebuggingLinksClicked } from "./computes/glue";

export class YarnApplicationTableWidget {
  currentNotebook: NotebookPanel | undefined;

  constructor() {
    this.currentNotebook = undefined;
  }
  // Callback for Notebook change signal.
  setListenerForNotebookChangeEvents(tracker: INotebookTracker) {
    tracker.currentChanged.connect((tracker, panel) => {
      if (panel !== null) {
        panel.node.addEventListener('DOMNodeInserted', () => {
          this.hookListenersIntoYarnTable();
        });
      }
    });
  }

  setCellExecutedSignal(): void {
    NotebookActions.executed.connect((sender, args) => {
      const { cell } = args;
      if (cell.model.type === 'code') {
        this.hookListenersIntoYarnTable();
      }
    });
  }


  onNotebookChange(
    tracker: INotebookTracker,
    notebookPanel: NotebookPanel | null
  ) {
    // Checks if there is a new notebook that was switched to
    if (notebookPanel !== null) {
      notebookPanel.revealed.then(() => this.hookListenersIntoYarnTable());
      this.currentNotebook = notebookPanel;
    }
  }


  // This function looks for all YARN table in the Notebook and adds on click listeners
  hookListenersIntoYarnTable(): void {
    const widget = this;

    // Hook listeners for table created from EMR on EC2 compute
    $('table.session_info_table').each(function () {
      // Retrieve connection name from the Cell output.
      const currentTable = $(this);
      const regex = /(?:Create session|Session information table) for connection:\s*([^\n\r]*)/;
      // Get the containing output area
      const closestConnectionOutput = $(this).closest('.jp-OutputArea')
          // Find all text outputs
          .find('.jp-RenderedText')
          // Filter for ones with connection name
          .filter(function() {
            return $(this).text().match(regex) !== null;
          })
          .filter(function() {        // Further filter to only get elements before current table
            return $(this).closest('.jp-OutputArea-child').index() <
                currentTable.closest('.jp-OutputArea-child').index();
          })
          .last();
      const match = closestConnectionOutput.text().match(regex);
      let connectionName = '';
      if (match && match.length > 1) {
        connectionName = match[1];
        connectionName = connectionName.trim();
      }

      // Set listener and metadata for spark ui link.
      let appId = $(this).find('td:nth-child(1)').text().trim();
      let sparkUiLink = $(this).find('td:nth-child(2) a');
      let attr = sparkUiLink.attr('connection_name');
      if (attr == undefined || attr == "") {
        sparkUiLink.addClass('spark-ui-link');
        sparkUiLink.attr('application_id', appId);
        sparkUiLink.attr('connection_name', connectionName);
        sparkUiLink.attr('link_type', LINK_TYPE_SPARK_UI);
        sparkUiLink.off('click').on('click', widget.onDebuggingLinkClicked);
      }

      // Set listener and metadata for driver log link
      const driverLogLink = $(this).find('td:nth-child(3) a');
      attr = driverLogLink.attr('connection_name');
      if (attr == undefined || attr == "") {
        driverLogLink.addClass('driver-log-link');
        driverLogLink.attr('application_id', appId);
        driverLogLink.attr('connection_name', connectionName);
        driverLogLink.attr('link_type', LINK_TYPE_DRIVER_LOG);
        driverLogLink.off('click').on('click', widget.onDebuggingLinkClicked);
      }
    });
  }

  // Callback for when debugging links are clicked.
  onDebuggingLinkClicked(event: any): void {
    event.preventDefault();
    const row = $(this).parent('td');
    row.addClass('loading-pau');
    const link = $(this);

    try {
      const applicationId = (link.attr('application_id') || '').trim();
      const connectionName = (link.attr('connection_name') || '').trim();
      const linkType = (link.attr('link_type') || '').trim();
      let logsLocation = (link.attr("log_location") || '').trim()

      if (applicationId == '') {
        console.error('Could not determine application id.');
        return;
      }

      if (connectionName == '') {
        console.error('Could not determine connection name.');
        return;
      }

      getConnectionDetails(connectionName)
        .then(connectionDetail => {

          if (connectionDetail.props.sparkGlueProperties) {
            handleGlueDebuggingLinksClicked(connectionDetail, applicationId, linkType, logsLocation)
              .finally(() => {
                row.removeClass('loading-pau');
              });
            return;
          } else if (connectionDetail.props.sparkEmrProperties) {

            // Handle EMR (EMR EC2 or EMR serverless).
            const parts = connectionDetail.props.sparkEmrProperties.computeArn.split('/');
            const computeId = parts[parts.length - 1];

            // Check if compute is an EMR on EC2 cluster, if not then treat it as a serverless application
            if (!computeId.startsWith('j-')) {
              handleEMRServerlessDebuggingLinksClicked(connectionDetail, applicationId, linkType)
                .finally(() => {
                  row.removeClass('loading-pau');
                });
            } else {
              handleEMRonEc2DebuggingLinksClicked(connectionDetail, applicationId, linkType, logsLocation)
                .finally(() => {
                  row.removeClass('loading-pau');
                });
            }
          } else {
            console.log("Unknown Spark compute.")
          }
        })
        .catch(e => {
          console.error(e);
        });
    } catch (e) {
      console.error(e);
    }
  }
}
