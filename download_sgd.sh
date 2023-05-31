mkdir data
cd data
git clone https://github.com/google-research-datasets/dstc8-schema-guided-dialogue.git
mv dstc8-schema-guided-dialogue/ dstc8
mkdir dstc8-schema-guided-dialogue
mv ./dstc8/train ./dstc8-schema-guided-dialogue/
mv ./dstc8/dev dstc8-schema-guided-dialogue/
mv ./dstc8/test dstc8-schema-guided-dialogue/
rm -rf dstc8