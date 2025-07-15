from app.modules.routes.index_manager import IndexManager

if __name__ == '__main__':
    result = IndexManager.update_index()
    if result['success']:
        print(f"インデックス更新成功！処理した文書数: {result['document_count']}（所要時間: {result['time']:.2f}秒）")
    else:
        print(f"インデックス更新失敗: {result['error']}")