import React, { Component } from 'react'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import './App.css'
import Dashboard from './components/Dashboard'
import rootReducer from './reducers'

const store = createStore(rootReducer, applyMiddleware(thunk))

class App extends Component {
  render () {
    return (
      <Provider store={store}>
        <div className='App'>
          <header className='App-header'>
            {/* <img src={logo} className='App-logo' alt='logo' /> */}
            <h1 className='App-title'>Hacktoberfest in Bucharest 2018</h1>
            <p>Pull request statistics at a glance</p>
          </header>
          <Dashboard />
        </div>
      </Provider>
    )
  }
}

export default App
