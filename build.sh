echo "Switching to project directory"
cd "$(dirname "$(readlink -f "$0")")"

echo "building frontend"
cd frontend
npm install
npm run build
cd ..

echo "cleanup target directory"
rm -rfv HuggingFace/flower-classification/{Dockerfile,app.py,class_names.json,frontend}

echo "copy built files"
cp -v Dockerfile HuggingFace/flower-classification/
cp -v app.py HuggingFace/flower-classification/
cp -v class_names.json HuggingFace/flower-classification/
cp -rv frontend/dist HuggingFace/flower-classification/frontend

echo "success"
