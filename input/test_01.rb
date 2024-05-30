require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns a list of items' do
    get '/api/items'
    expect(response).to have_http_status(200)
    expect(response.body).to include('item1', 'item2')
  end

  it 'creates an item' do
    post '/api/items', params: { item: { name: 'item3' } }
    expect(response).to have_http_status(201)
    expect(response.body).to include('item3')
  end
end