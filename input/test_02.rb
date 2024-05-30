require 'rails_helper'

RSpec.describe 'API', type: :request do
  it 'returns details of an item' do
    get '/api/items/1'
    expect(response).to have_http_status(200)
    expect(response.body).to include('item1')
  end

  it 'updates an item' do
    put '/api/items/1', params: { item: { name: 'updated_item1' } }
    expect(response).to have_http_status(200)
    expect(response.body).to include('updated_item1')
  end
end
