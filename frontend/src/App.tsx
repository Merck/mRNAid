import {Layout, Menu} from 'antd'
import * as React from 'react'
// eslint-disable-next-line import/named
import {RouteComponentProps, Route, Switch, withRouter, Link} from 'react-router-dom'

import withJobStore, {WithJobStore} from './utils/withJobStore'
import Index from './pages/index'
import './App.css'

type AppInnerProps = WithJobStore & RouteComponentProps

const POLL_INTERVAL = 1000

const getCurrentRootPath = (): string => {
  const chunks = window.location.pathname.split('/')
  return chunks.length > 1 ? chunks[1] : '/'
}

const App: React.FC<AppInnerProps> = ({getJob, submitRequest, requestJobResult}) => (
  <Layout>
    <Layout.Header>
      <Menu mode="horizontal" defaultSelectedKeys={[getCurrentRootPath()]} className="HeaderMenu HeaderFont">
        <Menu.Item key="mrnaid">
          <Link to="/">mRNAid</Link>
        </Menu.Item>
      </Menu>

      <Menu mode="horizontal" defaultSelectedKeys={[getCurrentRootPath()]} className="HeaderMenu version">
        <Menu.Item>
          <a href="https://github.com/Merck/mRNAid/issues">Report an issue</a>
        </Menu.Item>
        <Menu.Item>Version: 1.0.0</Menu.Item>
      </Menu>
    </Layout.Header>

    <Layout.Content className="container">
      <Switch>
        <Route
          exact
          path="/:id?"
          render={(routeParams) => {
            const jobId = routeParams.match.params.id
            return (
              <Index
                jobId={jobId}
                jobData={getJob(jobId)}
                submitRequest={submitRequest}
                requestJobResult={requestJobResult}
                pollInterval={POLL_INTERVAL}
              />
            )
          }}
        />
      </Switch>
    </Layout.Content>
  </Layout>
)

/**
 * `withRouter` is added in order to fix blocked updates
 * (as described here https://github.com/
 * ReactTraining/react-router/blob/master/packages/react-router/docs/guides/blocked-updates.md)
 */
export default withRouter(withJobStore(App))
